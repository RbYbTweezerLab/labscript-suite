#####################################################################
#                                                                   #
# /labscript_devices/TCPDH_Synth/blacs_worker.py                    #
#                                                                   #
#                                                                   #
#                                                                   #
# This file is part of labscript_devices, in the labscript suite    #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################
from asyncio.log import logger
# import logging
from formatter import NullFormatter
from os import times
import re
import select, socket
import time
import labscript_utils.h5_lock
import h5py
import numpy as np
from blacs.tab_base_classes import Worker
from labscript_utils.connections import _ensure_str
import labscript_utils.properties as properties


class TCPDH_SynthWorker(Worker):
    def init(self):
        # logging.basicConfig(level=logging.DEBUG)
 #       global serial; import serial
        global socket; import socket
        global h5py; import labscript_utils.h5_lock, h5py 
        self.smart_cache = {'STATIC_DATA': None, 'TABLE_DATA': '','CURRENT_DATA':None}
        self.server_address = (self.TCPIP_address,self.TCPIP_port)
        
        # conversion dictionaries if you choose different
        # base units. Used, eg. in program_static  The are
        # set to 1 now, so that there is no conversion. It
        # might be more efficient to work in kHz, so you 
        # need to send three less digits on the frequencies.
        # but for now we program device Hz --> Hz
        self.conv = {'freq':1}
        # read from device conversion, Hz --> Hz
        self.read_conv = {'freq':1}

        # populate the 'CURRENT_DATA' dictionary    
        self.check_remote_values()
        # self.smart_cache['CURRENT_DATA'] = {
        #     'PDH_carrier': {'freq': 1500000000},
        #     'PDH_mod': {'freq': 3125000, 'phase' : 0}
        # }
        self.program_manual(self.smart_cache['CURRENT_DATA'])
        # self.program_static(0,'freq',1000000000)
        # self.program_static(1,'freq',3125000)
        # self.program_static(1,'phase',0)


    ####################################################################
    # This function handles communication with the TCPDH Synth server.
    # The server sets the appropriate parameters on the RedPitaya and the
    # PLL/Teensy, and returns a string.  You don't need to use the returned
    # string, but it is useful in synchronizing the handshake with the 
    # server.
    def TCPDHsendinstr(self,instr):
        clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        #server_address = ('192.168.1.62', 6750)
        try:
            clientsock.connect(self.server_address)
        except ConnectionRefusedError as msg:
            self.logger.debug(f"ConnectionRefusedError: server {self.server_address} is most likely down.")
            raise
        #try:
        clientsock.send(instr.encode())
        #except:
        returnstr = ""
        returnstr_buff = ''
        readable, writable, exceptional = select.select(
                [clientsock], [], [clientsock])
        returnstr_buff = (clientsock.recv(2048)).decode()
        returnstr += returnstr_buff

        while returnstr_buff[-1] != '\r':
            returnstr_buff = (clientsock.recv(2048)).decode()
            returnstr += returnstr_buff
            # readable, writable, exceptional = select.select(
                # [clientsock], [clientsock], [clientsock])
        # if instr[-1] == '\r':
        clientsock.close()
        if returnstr[0:2] == 'ER':
            msg = '''Instruction "%s" did not execute properly.'''%instr
            raise Exception(msg)
        print("TCPDHsendinstr: "+ returnstr[0:50])
        return returnstr
    
    def check_connection(self):
        #pass
        """Sends non-command and tests for correct response, returns True if connection
        appears to be working correctly, else returns False. Needs to check both the 
        Red Pitaya and the PLL board NOT USED ANYWHERE I CAN FIND"""
        try:
            return self.TCPDHsendinstr("Q?;") != ''
        except IndexError:
                #     # empty response, probably not connected
             return False

# This is used automatically by labscript in various conditions
# It is called every couple of seconds while idle to m
    def check_remote_values(self):
        # Get the currently output values:
        resp = self.TCPDHsendinstr('Q?;').split(';')
        while resp[-1] == '':
            resp.pop(-1)
        print("Check remote values:  ")
        print(resp)

        results = {}
        results['PDH_carrier'] = {}
        results['PDH_mod']={}
        results['PDH_carrier']['freq']=round((float(resp[0].split()[1])*self.read_conv['freq']+0.5))
        print(results['PDH_carrier']['freq'])
        results['PDH_mod']['freq']= round(float(resp[1].split()[1])*self.read_conv['freq']+0.5)
        results['PDH_mod']['phase']=round(float(resp[2].split()[1])+0.5)
            
        self.smart_cache['CURRENT_DATA'] = results
        print(self.smart_cache['CURRENT_DATA'])
        return results
   
    def program_manual(self,front_panel_values):
        # TODO: Optimise this so that only items that have changed are reprogrammed by storing the last programmed values
        response = ""
        self.smart_cache['STATIC_DATA'] = front_panel_values
        if self.smart_cache['CURRENT_DATA']['PDH_carrier']['freq'] != front_panel_values['PDH_carrier']['freq']:
            response = self.program_static(0,'freq',front_panel_values['PDH_carrier']['freq']*self.conv['freq'])
        if self.smart_cache['CURRENT_DATA']['PDH_mod']['freq'] != front_panel_values['PDH_mod']['freq']:
            response +=  ';' + self.program_static(1,'freq',front_panel_values['PDH_mod']['freq']*self.conv['freq'])
        if self.smart_cache['CURRENT_DATA']['PDH_mod']['phase'] != front_panel_values['PDH_mod']['phase']:
            response = response + ';' + self.program_static(1,'phase',front_panel_values['PDH_mod']['phase'])
        # if response != "":
            # self.smart_cache['STATIC_DATA'] = None

        # # # Now that a static update has been done, we'd better invalidate the saved STATIC_DATA:
        # self.smart_cache['STATIC_DATA'] = None
        # response = self.TCPDHsendinstr('Q?')
        # respList = response.split(';')
        # if respList[-1]=='':
        #     respList.pop(-1)
        # print('program_manual response:  ')
        # print(respList)
        front_panel_values= self.check_remote_values()
        return front_panel_values

    def generate_manual_instr_string(self,channel,type,value):
        instruct = ''
        if channel == 0: #carrier
            if type == 'freq': #
                instruct = 'FC {};'.format(int(value))
            else:
                raise TypeError(type)
        if channel == 1: # modulation
            if type == 'freq':
                instruct = 'FM %d;'%(value)
            elif type == 'phase':
                instruct = 'PM %d;'%(value)
            else:
                raise TypeError(type)
        return instruct

    def program_static(self,channel,type,value):
        instr=self.generate_manual_instr_string(channel,type,value)
        return self.TCPDHsendinstr(instr+'\r')
        
            
    def transition_to_buffered(self,device_name,h5file,initial_values,fresh):
        # Store the initial values in case we have to abort and restore them:
        self.initial_values = initial_values
        print('Initial values:')
        print(self.initial_values)
        #print(type(self.initial_values['PDH_carrier']['freq'] ))
        # Store the final values to for use during transition_to_static:
        self.final_values = {}
        static_data = None
        table_data = None
        change_times = None
        ramp_times = None
        with h5py.File(h5file, 'r') as hdf5_file:
            group = hdf5_file['/devices/'+device_name]
            # If there are values to set the unbuffered outputs to, set them now:
            if 'STATIC_DATA' in group:
                static_data = group['STATIC_DATA'][:][0]
            # Now program the buffered outputs:
            if 'TABLE_DATA' in group:
                table_data = group['TABLE_DATA'][:]
            if 'CHANGE_TIMES' in group:
                change_times = group['CHANGE_TIMES'][:].tolist()
            if 'RAMP_TIMES' in group:
                ramp_times = group['RAMP_TIMES'][:].tolist()
 
            group = hdf5_file['/devices/'+device_name]   # Get the timing data from the pseudoclock, 
            if 'CLOCK_DATA' in group:                # needed to properly program the PLL/Synth
                clock_data = group['CLOCK_DATA'][:]   # The timing data is in the format (Period, repetitions) 
            if 'INSTR_DATA' in group:
                instr_data = group['INSTR_DATA'][:]

        if static_data is not None:
            data = static_data
            if True: #fresh or data != self.smart_cache['STATIC_DATA']:
                self.logger.debug('Static data has changed, reprogramming.')
                self.smart_cache['STATIC_DATA'] = data
                self.TCPDHsendinstr('FM {};PM {}\r'.format(str(data['freq']),str(data['phase'])))
                
                # Save these values into final_values so the GUI can
                # be updated at the end of the run to reflect them:                
                self.final_values['PDH_mod'] = {}
                self.final_values['PDH_mod']['freq'] = data['freq']
                self.final_values['PDH_mod']['phase'] = data['phase'] 

        # Now program the buffered outputs:
        if table_data is not None:
            data = table_data

            # # at some point we should fix this smart cache so that it doesn't reprogram if there are no changes.
            # if True: #fresh or data != self.smart_cache['TABLE_DATA']:
            #     self.logger.debug('Table data has changed, reprogramming.')

            #     # First, get a list of "ramps", which includes real ramps and also equally spaced set constants:
            #     nreplist0 =[clock_data[i][1] for i in range(len(clock_data))] # the number of repetitions of the "ramp"
            #     rampIndex0 = [sum(nreplist0[:ri])+ri for ri in range(len(nreplist0))] #the index in table_data of the "ramp"
            
            #     #find the position of the *true* ramps:
            #     realramps = []
            #     if ramp_times != []:
            #         for tramp in ramp_times:
            #             realramps.append(change_times.index(tramp[0]))

            #     # now calculate the real nrep and rampIndex for *real* ramps            
            #     nreplist = []
            #     for ri,nrep in zip(rampIndex0, nreplist0):
            #         if nrep>0 and (ri not in realramps):
            #             expand = [0 for j in range( nrep+1)] # expand the ramp into nrep+1 single steps (nrep=0)
            #             nreplist = nreplist + expand     #add the expanded single steps to the nreplist
            #         else:
            #             nreplist  = nreplist +[nrep]

            #     # now create the list of indices in table_data where the *real* ramps start:

            #     rampIndex = []
            #     nreps_i = 0
            #     nreplist= []
            #     for i in range(len(instr_data)):
            #         print(instr_data[i][0],instr_data[i][3])
            #         # if instr_data[i][0] == 1:
            #         rampIndex.append(int(i+nreps_i))
            #         nreps_i += instr_data[i][3]-1
            #         nreplist.append(int(instr_data[i][3]))
            #     # nreplist.append(-1)
            #     # rampIndex = [sum( nreplist[:ri])+ri for ri in range(0,len(nreplist))]

            #     rampfreqs = [float(data[rampIndex[ri]][0]) for ri in range(len(rampIndex))] if rampIndex != [] else []
            #     print("rampfreqs: ",rampfreqs)
            #     # deltafreqs = [(round((rampfreqs[ri+1]-rampfreqs[ri])/(nreplist[ri]+0.5)+0.5) if nreplist[ri]!=0 else 0)  for ri in range(len(nreplist)-1)]+[0]
            #     deltafreqs = [int(round((rampfreqs[ri+1]-rampfreqs[ri])/(nreplist[ri])))  for ri in range(len(nreplist)-1)]+[0]
            #     #convert to integers and make deltafreqs strictly positive with scanUP containing the scan direction
            #     rampfreqs = [int(round(freq +0.5)) for freq in rampfreqs]            
            #     scanUP = [int(dfreq > 0) for dfreq in deltafreqs]
            #     deltafreqs = [int(abs(dfreq)) for dfreq in deltafreqs]
            #     # write the data string
            #     datastr = ''
            #     for i, freq in enumerate(rampfreqs):
            #         newstr = str(freq)+','+str(deltafreqs[i])+','+str(nreplist[i])+','+str(scanUP[i])+',\t'
            #         datastr += newstr
            #         print(i,newstr)

            if True:
                datastr = '' 
                for i,freq in enumerate(table_data):
                    datastr += str(freq[0])
                    if i != len(table_data)-1:
                        datastr += ','
                self.TCPDHsendinstr("FT "+ datastr+'\r')
                print("Sending datastr: ...")

                # Store the table for future smart programming comparisons:
                try:
                    self.smart_cache['TABLE_DATA'][:len(data)] = data
                    self.logger.debug('Stored new table as subset of old table')
                except: # new table is longer than old table
                    self.smart_cache['TABLE_DATA'] = data
                    self.logger.debug('New table is longer than old table and has replaced it.')
                
                # Get the final values of table mode so that the GUI can
                # reflect them after the run:
                self.final_values['PDH_carrier'] = {}
                self.final_values['PDH_carrier']['freq'] = data[-1]['freq']

            # Transition to table mode:
            if self.update_mode == 'synchronous':
                print("Made it to before TT:\n")
                self.TCPDHsendinstr('TT\r')
                print("Made it to after TT:\n")
            elif self.update_mode == 'asynchronous':
                pass
            else:
                raise ValueError('invalid update mode %s'%str(self.update_mode))

        print(self.final_values)
        return self.final_values
    
    def abort_transition_to_buffered(self):
        return self.transition_to_manual(True)
        
    def abort_buffered(self):
        # TODO: untested
        return self.transition_to_manual(True)
    
    def transition_to_manual(self,abort = False):
        print("before TM sent")
        self.TCPDHsendinstr('TM\r')
        print("TM send inside trans. to manual")
        if abort:
            # If we're aborting the run, then we need to reset DDSs 2 and 3 to their initial values.
            # 0 and 1 will already be in their initial values. We also need to invalidate the smart
            # programming cache for them.
            values = self.initial_values
            self.program_static(0,'freq',values['PDH_carrier']['freq'])            
            # self.program_static(1,'freq',values['PDH_mod']['freq'])
            # self.program_static(1,'phase',values['PDH_mod']['phase'])
            self.smart_cache['STATIC_DATA'] = None
        else:
            # If we're not aborting the run, then we need to set DDSs 0 and 1 to their final values.
            # 2 and 3 will already be in their final values.
            values = self.final_values
            self.program_static(0,'freq',values['PDH_carrier']['freq'])
            # self.program_static(1,'freq',values['PDH_mod']['freq'])
            # self.program_static(1,'phase',values['PDH_mod']['phase'])
        return True

    def shutdown(self):
        pass
        # self.connection.close()
        
     