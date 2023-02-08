#####################################################################
#                                                                   #
# /labscript_devices/FPGA_Synth/blacs_tab.py                        #
#                                                                   #
# Copyright 2021, Philip Starkey; edited by Oliver Tu               #
#                                                                   #
# This file is part of labscript_devices, in the labscript suite    #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################
from blacs.device_base_class import (
    DeviceTab,
    define_state,
    MODE_BUFFERED,
    MODE_MANUAL,
    MODE_TRANSITION_TO_BUFFERED,
    MODE_TRANSITION_TO_MANUAL,
)
import labscript_utils.properties

from qtutils.qt import QtWidgets

class FPGA_SynthTab(DeviceTab):
    def initialise_GUI(self):        
        self.units =    {'freq':'Hz',      'amp':'Arb'}
        self.min =      {'freq':1,      'amp':0}
        self.max =      {'freq':5e8,      'amp':1} 
        self.step =     {'freq':10000,      'amp':0.1}
        self.decimals = {'freq':0,         'amp':3} 
        
        # Create DDS Output objects: we only need frequency for the carrier and frequency and phase for the mod
        dds_prop = {}
        subchnl = 'freq'
        dds_prop['DDS_channel']={}
        dds_prop['DDS_channel'][subchnl]={'base_unit':self.units[subchnl],
                                                     'min':self.min[subchnl],
                                                     'max':self.max[subchnl],
                                                     'step':self.step[subchnl],
                                                     'decimals':self.decimals[subchnl]
                                                    }
        subchnl = 'amp'
        dds_prop['DDS_channel'][subchnl]={'base_unit':self.units[subchnl],
                                                     'min':self.min[subchnl],
                                                     'max':self.max[subchnl],
                                                     'step':self.step[subchnl],
                                                     'decimals':self.decimals[subchnl]
                                                    }
    #    Create the output objects    
        self.create_dds_outputs(dds_prop)        
        # Create widgets for output objects
        dds_widgets,ao_widgets,do_widgets = self.auto_create_widgets()
        # and auto place the widgets in the UI
        self.auto_place_widgets(("DDS settings",dds_widgets))
        
        connection_object = self.settings['connection_table'].find_by_name(self.device_name)
        connection_table_properties = connection_object.properties
        
        self.TCPIP_port = connection_table_properties.get('TCPIP_port', None)
        self.TCPIP_address = connection_table_properties.get('TCPIP_address', None)
        self.default_TCPIP_port = connection_table_properties.get('default_TCPIP_port', None)

        
        # Create and set the primary worker
        self.create_worker("main_worker",
                            'labscript_devices.FPGA_Synth.blacs_workers.FPGA_DDSWorker',
                            {'TCPIP_port':self.TCPIP_port,
                            'TCPIP_address': self.TCPIP_address,
                            'default_TCPIP_port': self.default_TCPIP_port})
        
        self.primary_worker = "main_worker"

        # Set the capabilities of this device
        self.supports_remote_value_check(False)
        self.supports_smart_programming(True) 
