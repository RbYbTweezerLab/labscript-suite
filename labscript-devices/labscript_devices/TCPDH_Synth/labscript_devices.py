#####################################################################
#                                                                   #
# /TCPDH_Synth.py                                                   #
#                                                                   #
#                                                                   #
#                                                                   #
# This file is part of the module labscript_devices, in the         #
# labscript suite (see http://labscriptsuite.org), and is           #
# licensed under the Simplified BSD License. See the license.txt    #
# file in the root of the project for the full license.             #
#                                                                   #
#####################################################################

from labscript_devices import runviewer_parser, BLACS_tab

from labscript import IntermediateDevice, DDSQuantity, StaticDDS, AnalogOut, Device, config, LabscriptError, set_passed_properties,compiler
from labscript_utils.unitconversions import TCPDH_SynthFreqConversion, TCPDH_SynthAmpConversion,TCPDH_SynthPhaseConversion

import numpy as np
import labscript_utils.h5_lock, h5py
import labscript_utils.properties

__version__ = '1.0.0'
__author__ = ['jvp']

class TCPDH_DDS(DDSQuantity):

    table = []
    pseudoclock_res = None
    srate = None
    def init_if_needed(self,t):
        if t==0:
            self.table = []

        self.pseudoclock_res = compiler.master_pseudoclock.clock_resolution
        print('Master pseudoclock device clock_resolution: ', self.pseudoclock_res)

    def set_freq(self, t, freq, units=None):
        print('TCPDH_DDS.setfreq(): compiling data table... ')
        self.init_if_needed(t)

        self.table.append([0,t,0,1]) # first element = instr_code: set_freq -> 0, ramp -> 1
        self.setfreq(t,freq, units=units)

    def ramp(self, t, duration, initial, final, samplerate, units=None, truncation=1.):
        print('TCPDH_DDS.ramp(): compiling data table... ')
        self.init_if_needed(t)
        self.srate = samplerate
        period = int(round(1./self.srate/self.pseudoclock_res))
        print(self.srate)
        print(1/self.srate)
        print(period)
        nreps = int(round(duration*self.srate)-1)
        self.table.append([1,t             , period, nreps]) # first element = instr_code: set_freq -> 0, ramp -> 1
        clk_err = int(round((int(round(1./self.srate/self.pseudoclock_res)) - 1./self.srate/self.pseudoclock_res)*(nreps+1)))
        self.table.append([1,t+period*nreps*self.pseudoclock_res, period - clk_err, 1])
        self.frequency.ramp(t, duration, initial, final, self.srate, units=units, truncation=truncation)

class TCPDH_StaticDDS(StaticDDS):
    test2 = 2 

class TCPDH_Synth(IntermediateDevice):
    """
    This class is initilzed with the key word argument
    'TCPIP_address',  -- 
    'TCPIP_port' -- 
    """
    description = 'TCPDH'
    allowed_children = [TCPDH_DDS, TCPDH_StaticDDS,AnalogOut]
    clock_limit = 9990 # 
    ALLOWED_FMOD = [500000, 625000, 781250, 1000000, 1250000, 1562500, 1953125, 2500000, \
                    3125000, 3906250, 5000000, 6250000, 7812500, 12500000]
    # 
    minimum_clock_high_time = 1e-6

    @set_passed_properties(
        property_names={
            'connection_table_properties': [
                'TCPIP_port',
              #  'default_TCPIP_port',
                'TCPIP_address',
                'update_mode',
            ],
        }
    )
    def __init__(
        self,
        name,
        parent_device,
        TCPIP_port=6750,
        TCPIP_address='192.168.1.133',
        update_mode='synchronous',
        synchronous_first_line_repeat=True,
        **kwargs
    ):
        IntermediateDevice.__init__(self, name, parent_device, **kwargs)
        self.BLACS_connection = '%s,%s'%(TCPIP_address, TCPIP_port)
        
        # Integer multiples of 125 kHz
        ALLOWED_FMOD =(500000, 625000, 781250 ,1000000, 1250000, 1562500, 1953125, 2500000,\
                3125000, 3906250, 5000000, 6250000, 7812500, 12500000,15625000, 15625000)

        if not (6700< int(TCPIP_port) < 65536):     
            raise LabscriptError('TCPIP_port must be in the range of 6700-65535')            
        
        self.update_mode = update_mode
        self.synchronous_first_line_repeat = synchronous_first_line_repeat        
 
    def add_device(self, device):
        Device.add_device(self, device)
        # The PDH driver doesn't work below 500 MHz
        device.frequency.default_value = 1e9 
            
    def get_default_unit_conversion_classes(self, device):
        """Child devices call this during their __init__ (with themselves
        as the argument) to check if there are certain unit calibration
        classes that they should apply to their outputs, if the user has
        not otherwise specified a calibration class"""
        return TCPDH_SynthFreqConversion, TCPDH_SynthAmpConversion, TCPDH_SynthPhaseConversion
    
    def quantise_fmod(self,fin,device):
        i=0
        while( -(self.ALLOWED_FMOD[i+1]-self.ALLOWED_FMOD[i])< 2*(fin-self.ALLOWED_FMOD[i+1]) and i+1< len(self.ALLOWED_FMOD)-1):
            i+=1
        return self.ALLOWED_FMOD[i],1

    def quantise_freq(self, data, device):
        """Provides bounds error checking and scales input values to instrument
        units (0.1 Hz) before ensuring uint64 integer type."""
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        # Ensure that frequencies are within bounds:
        if np.any(data > 2e9 )  or np.any(data < 0.5e9 ):  #base unit Hz
            raise LabscriptError('%s %s '%(device.description, device.name) +
                              'can only have frequencies between 500MHz and 2GHz, ' + 
                              'the limit imposed by %s.'%self.name)
        # It's faster to add 0.5 then typecast than to round to integers first:
        data = np.array((data)+0.5,dtype=np.uint64)
        scale_factor = 1
        return data, scale_factor
        
    def quantise_phase(self, data, device):
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        # ensure that phase wraps around:
        data %= 360
        # It's faster to add 0.5 then typecast than to round to integers first:
        data = np.array((data)+0.5,dtype=np.uint16)
        scale_factor = 1
        return data, scale_factor
        
    def quantise_amp(self,data,device):
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        # ensure that amplitudes are within bounds:
        if np.any(data > 1 )  or np.any(data < 0):
            raise LabscriptError('%s %s '%(device.description, device.name) +
                              'can only have amplitudes between 0 and 1 (Volts peak to peak approx), ' + 
                              'the limit imposed by %s.'%self.name)
        # It's faster to add 0.5 then typecast than to round to integers first:
        data = np.array((1023*data)+0.5,dtype=np.uint16)
        scale_factor = 1023
        return data, scale_factor
        
    def generate_code(self, hdf5_file):
        DDSs = {}
        # error check and make a list of the two devices:
        for output in self.child_devices:
            # Check that the instructions will fit into RAM:
            # if isinstance(output, TCPDH_DDS) and len(output.frequency.raw_output) > 5000 - 2: # -2 to include space for dummy instructions
            #     raise LabscriptError('%s can only support XXXX instructions. '%self.name +
            #                          'Please decrease the sample rates of devices on the same clock, ' + 
            #                          'or connect %s to a different pseudoclock.'%self.name)
            #channel = output.connection
            if output.connection == 'PDH_carrier':
                channel = 0
            elif  output.connection == 'PDH_mod':
                channel = 1
            else:
                raise LabscriptError('%s %s has invalid connection string: \'%s\'. '%(output.description,output.name,str(output.connection)) + 
                                     'Format must be either \'PDH_carrier\' or \'PDH_mod\' ')
            DDSs[channel] = output #DDSs[0]=PDH_carrier, DDSs[1] = PDH_mod    

        # make sure the DDSs are correct in number/type
        if (len(DDSs) != 2) or (DDSs[0].connection != 'PDH_carrier') or (DDSs[1].connection != 'PDH_mod'):
            raise LabscriptError('%s has wrong number/type of connections:  '%(self.description) + 
                                     'Must have one each of \'PDH_carrier\' \'PDH_mod\' ')

        # define the np.array table data structures:
        dtypes = {'names':['freq'],'formats':[np.uint64]}
        static_dtypes = {'names':['freq','phase'],'formats':[np.uint64,np.uint16]}

        clockline = self.parent_clock_line
        pseudoclock = clockline.parent_device
        times = pseudoclock.times[clockline]

        # set the tableable PDH_carrier dds first,  
        dds = DDSs[0]
        # convert the labscript-calculated values into frequency quantized versions:
        dds.frequency.raw_output, dds.frequency.scale_factor = self.quantise_freq(dds.frequency.raw_output, dds)
        out_table = np.zeros(len(times),dtype=dtypes)# create the table data for the hdf5 file.
        out_table['freq'].fill(1) # set them to 1
        out_table['freq'][:] = dds.frequency.raw_output
        change_times = dds.frequency.get_change_times()    
        ramp_times = dds.frequency.get_ramp_times()    
        timeseries = times

        # Then do the 
        dds = DDSs[1]
        print("In generate_code(): PDH_mod freq. = ",dds.frequency.raw_output)
        dds.frequency.raw_output, dds.frequency.scale_factor = self.quantise_fmod(dds.frequency.raw_output, dds)
        dds.phase.raw_output, dds.phase.scale_factor = self.quantise_phase(dds.phase.raw_output, dds)
        static_table = np.zeros(1, dtype=static_dtypes)
        static_table['freq'].fill(1)
        static_table['freq'] = dds.frequency.raw_output
        static_table['phase'] = dds.phase.raw_output

        grp = self.init_device_group(hdf5_file)
        grp.create_dataset('TABLE_DATA',compression=config.compression,data=out_table) 
        grp.create_dataset('STATIC_DATA',compression=config.compression,data=static_table) 
        grp.create_dataset('CHANGE_TIMES',compression = config.compression,data=change_times)
        grp.create_dataset('RAMP_TIMES',compression = config.compression,data=ramp_times)
        grp.create_dataset('TIMES',compression = config.compression,data=timeseries)
        
        # Iterate through the table and add durations to the set_freq entries:
        for i in range(len(DDSs[0].table)-1):
            if DDSs[0].table[i][2] == 0:
                DDSs[0].table[i][2] = (DDSs[0].table[i+1][1] - DDSs[0].table[i][1])/DDSs[0].pseudoclock_res
        
        if DDSs[0].table[-1][0] == 1 and timeseries[-1] != DDSs[0].table[-1][1]:
            raise LabscriptError('%s ends sequence with a ramp.  '%(self.description) + 
                                     'Please end labscript sequence with set_freq().')
        else:
            DDSs[0].table[-1][2] = 40

        for i in range(len(DDSs[0].table)-1):
            dt_ramp = DDSs[0].table[i][2]*DDSs[0].table[i][3]*DDSs[0].pseudoclock_res
            time_diff = (DDSs[0].table[i+1][1]-DDSs[0].table[i][1]) - dt_ramp
            print(i,time_diff)
            if np.abs(time_diff) >= DDSs[0].pseudoclock_res:
                DDSs[0].table.insert(i+1,[0,DDSs[0].table[i][1]+dt_ramp,time_diff/DDSs[0].pseudoclock_res,1])

        grp.create_dataset('INSTR_DATA',compression=config.compression,data=DDSs[0].table)

        clock_data_table = []

        for i in range(len(DDSs[0].table)):
            clock_data_table.append(DDSs[0].table[i][2:])
        
        clock_data_table.append([0,0])
        clock_data_table = np.array(clock_data_table,dtype=int)
        print(clock_data_table)
        grp.create_dataset('CLOCK_DATA',compression=config.compression,data=clock_data_table)

        self.set_property('frequency_scale_factor', 1, location='device_properties')
        self.set_property('amplitude_scale_factor', 1, location='device_properties')
        self.set_property('phase_scale_factor',1, location='device_properties')

