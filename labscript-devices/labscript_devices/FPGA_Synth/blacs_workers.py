#####################################################################
#                                                                   #
# /labscript_devices/FPGA_DDS/blacs_worker.py                       #
#                                                                   #
# This file is part of labscript_devices                            #
#                                                                   #
#####################################################################
from asyncio.log import logger
import logging
from formatter import NullFormatter
from os import times
import re
import select, socket
import labscript_utils.h5_lock
import h5py
import numpy as np
from blacs.tab_base_classes import Worker
from labscript_utils.connections import _ensure_str
import labscript_utils.properties as properties
from struct import pack
from time import time
import sys
from time import sleep


class FPGA_DDSWorker(Worker):
    def init(self):
        # logging.basicConfig(level=logging.DEBUG) # Use this line to debugging 
        global socket; import socket
        global h5py; import labscript_utils.h5_lock, h5py 
        self.smart_cache = np.array([-1])
        self.server_address = (self.TCPIP_address,self.TCPIP_port)
        
        self.set_default(0.5,100000000)

    def FPGAsendinstr(self,instr):
        # print("time when sending started:"+str(time())+"\n")
        clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            clientsock.connect(self.server_address)
        except ConnectionRefusedError as msg:
            self.logger.debug(f"ConnectionRefusedError: server {self.server_address} is most likely down.")
            raise
        # i = 0
        # trunc_len= 2000
        # truncated_instr = instr[0:trunc_len]
        # while len(truncated_instr)>0:
        #     clientsock.send(truncated_instr)
        #     truncated_instr=instr[i*trunc_len:(i+1)*trunc_len]
        #     i+=1
        #     sleep(0.2)
        clientsock.sendall(instr)
        # response = clientsock.recv(1024)
        print("time when sending finished:"+str(time())+"\n")
        print("size of data should be sent:" + str(sys.getsizeof(instr))+"\n")
        # print("response:"+str(response))
        return 'ok'
   
    def program_manual(self,front_panel_values):
        self.program_static('amp',front_panel_values['DDS_channel']['amp'])
        self.program_static('freq',front_panel_values['DDS_channel']['freq'])
        return front_panel_values

    def generate_manual_instr_string(self,type,value):
        if type == 'freq':
            instruct = b'\xff\xff\xff\x02'+ pack('>L',int(value * (2 ** 32-1) / 1e9))
        elif type == 'amp':
            instruct = b'\xff\xff\xff\x04' + pack('>L',int(value * (2 ** 20-1)))
        else:
                raise TypeError(type)
        return instruct

    def program_static(self,type,value):
        instr=self.generate_manual_instr_string(type,value)
        return self.FPGAsendinstr(instr)
        
    def set_default(self,default_amp,default_freq):
        self.program_static('amp',default_amp)
        self.program_static('freq',default_freq)

    def transition_to_buffered(self,device_name,h5file,initial_values,fresh):
        # Store the initial values in case we have to abort and restore them:
        self.initial_values = initial_values
        self.final_values = {}
        table_data = None
        print("time when started reading h5file:"+str(time())+"\n")
        with h5py.File(h5file, 'r') as hdf5_file:
            group = hdf5_file['/devices/'+device_name]
            if 'TABLE_DATA' in group:
                table_data = group['TABLE_DATA'][:]

        # Now program the buffered outputs:
        # print("time when ended reading h5file:"+str(time())+"\n")
        if table_data is not None:
            if not np.array_equal(self.smart_cache, table_data):
                data = table_data
                amp_string = data['amp'][:]
                freq_string = data['freq'][:]
                data_num = len(amp_string)
                phase_string = np.zeros(data_num,dtype = np.uintc)
                body_bulk = np.transpose(np.array([amp_string,freq_string,phase_string],dtype=np.uintc)).flatten()
                finaltable = b'\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00' # Heading
                finaltable += pack('>%sL' % len(body_bulk),*body_bulk) # Generate unsigned 32-bit integer type hex string in big-endian
                finaltable += b'\xff\xff\xff\xfe' # Ending
                self.FPGAsendinstr(finaltable)
                self.smart_cache = data
                self.final_values['FPGA_DDS'] = {}
                self.final_values['FPGA_DDS']['freq'] = data[-1]['freq']
                self.final_values['FPGA_DDS']['amp'] = data[-1]['amp']
            else:
                print('Skip reprogramming due to smart_cache')

        # print(self.final_values)
        return self.final_values
    
    def abort_transition_to_buffered(self):
        return self.transition_to_manual(True)
        
    def abort_buffered(self):
        return self.transition_to_manual(True)
    
    def transition_to_manual(self,abort = False):
        return True

    def shutdown(self):
        pass

     
