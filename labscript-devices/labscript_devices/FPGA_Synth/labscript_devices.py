#####################################################################
#                                                                   #
# /FPGA_Synth.py                                                   #
#                                                                   #
#                                                                   #
#                                                                   #
# This file is part of the module labscript_devices, in the         #
# labscript suite (see http://labscriptsuite.org), and is           #
# licensed under the Simplified BSD License. See the license.txt    #
# file in the root of the project for the full license.             #
#                                                                   #
#####################################################################


from labscript_devices import runviewer_parser

from labscript import IntermediateDevice, DDSQuantity, Device, config, LabscriptError, set_passed_properties
from labscript_utils.unitconversions import FPGA_SynthFreqConversion, FPGA_SynthAmpConversion
import labscript_utils.properties
import numpy as np
import time

__author__ = ['Oliver Tu']

class FPGA_DDS(DDSQuantity):
    def set_param(self, t, freq, amp, units=None):
        print('FPGA_DDS.setfreq(): compiling data table... ')
        self.setfreq(t,freq, units=units)
        self.setamp(t,amp, units=units)

    def ramp(self, t, duration, initial_freq, final_freq, initial_amp, final_amp, samplerate, units=None, truncation=1.):
        print('FPGA_DDS.ramp(): compiling data table... ')
        self.frequency.ramp(t, duration, initial_freq, final_freq, samplerate, units=units, truncation=truncation)
        self.amplitude.ramp(t, duration, initial_amp, final_amp, samplerate, units=units, truncation=truncation)

class FPGA_Synth(IntermediateDevice):
    """
    This class is initilzed with the key word argument
    'TCPIP_address',  -- 
    'TCPIP_port' -- 
    """
    description = 'FPGA'
    allowed_children = [FPGA_DDS]

    @set_passed_properties(
        property_names={
            'connection_table_properties': [
                'TCPIP_port',
                'TCPIP_address',
                
            ]
        }
    )
    def __init__(
        self,
        name,
        parent_device,
        TCPIP_port=5000,
        TCPIP_address='192.168.1.103',
        **kwargs
    ):
        IntermediateDevice.__init__(self, name, parent_device, **kwargs)
        self.BLACS_connection = '%s,%s'%(TCPIP_address, TCPIP_port)     
    def add_device(self, device):
        Device.add_device(self, device)
        device.frequency.default_value = 1e8
        device.amplitude.default_value = 0.5 
            
    def get_default_unit_conversion_classes(self, device):
        """Child devices call this during their __init__ (with themselves
        as the argument) to check if there are certain unit calibration
        classes that they should apply to their outputs, if the user has
        not otherwise specified a calibration class"""
        return FPGA_SynthFreqConversion, FPGA_SynthAmpConversion, None
    
    def quantise_freq(self, data, device):
        """Provides bounds error checking and scales input values to instrument
        units (0.1 Hz) before ensuring uint32 integer type."""
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        # Ensure that frequencies are within bounds:
        if np.any(data > 5e8 )  or np.any(data < 1 ):  #base unit Hz
            raise LabscriptError('%s %s '%(device.description, device.name) +
                              'can only have frequencies between 500MHz and 1Hz, ' + 
                              'the limit imposed by %s.'%self.name)
        scale_factor = (2 ** 32 - 1 )/ 1e9
        data = np.array(data * scale_factor,dtype=np.uint32)
        return data
        
    def quantise_amp(self,data,device):
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        # ensure that amplitudes are within bounds:
        if np.any(data > 1 )  or np.any(data < 0):
            raise LabscriptError('%s %s '%(device.description, device.name) +
                              'can only have amplitudes between 0 and 1, ' + 
                              'the limit imposed by %s.'%self.name)
        scale_factor = 2 ** 20 - 1
        data = np.array(scale_factor*data,dtype=np.uint32)
        return data
        
    def generate_code(self, hdf5_file):
        DDSs = {}
        # error check and make a list of the two devices:
        for output in self.child_devices:
            # Check that the instructions will fit into RAM:
            # if isinstance(output, FPGA_DDS) and len(output.frequency.raw_output) > 5000 - 2: # -2 to include space for dummy instructions TODO: check the RAM
            #     raise LabscriptError('%s can only support XXXX instructions. '%self.name +
            #                          'Please decrease the sample rates of devices on the same clock, ' + 
            #                          'or connect %s to a different pseudoclock.'%self.name)
            DDSs[0] = output #DDSs[0]=PDH_carrier, DDSs[1] = PDH_mod    

        dtypes = {'names':['freq','amp'],'formats':[np.uint32,np.uint32]}

        clockline = self.parent_clock_line
        pseudoclock = clockline.parent_device
        times = pseudoclock.times[clockline]
        # print("time when started preparing h5file:"+str(time.time())+"\n")
        dds = DDSs[0]
        dds.frequency.raw_output = self.quantise_freq(dds.frequency.raw_output, dds)
        dds.amplitude.raw_output = self.quantise_amp(dds.amplitude.raw_output, dds)
        # print('time when ramp finished:'+str(time.time()))
        out_table = np.zeros(len(times),dtype=dtypes)# create the table data for the hdf5 file.
        out_table['freq'].fill(1) # set them to 1
        out_table['freq'][:] = dds.frequency.raw_output
        out_table['amp'].fill(1) # set them to 1
        out_table['amp'][:] = dds.amplitude.raw_output
        # print("time when started creating h5file:"+str(time.time())+"\n")
        grp = self.init_device_group(hdf5_file)
        grp.create_dataset('TABLE_DATA',compression=config.compression,data=out_table) 
        print("time when ended creating h5file:"+str(time.time())+"\n")
