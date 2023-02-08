#####################################################################
#                                                                   #
# /labscript_devices/PrawnBlaster/blacs_tab.py                      #
#                                                                   #
# Copyright 2021, Philip Starkey                                    #
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

class TCPDH_SynthTab(DeviceTab):
    def initialise_GUI(self):        
        self.carrier_base_units =    {'freq':'Hz',      'phase':'Degrees'}
        self.carrier_base_min =      {'freq':500e6,      'phase':0}
        self.carrier_base_max =      {'freq':2000e6,      'phase':360} 
        self.carrier_base_step =     {'freq':0.010e6,      'phase':10}
        self.carrier_base_decimals = {'freq':0,         'phase':0} 
        self.mod_base_units =    {'freq':'Hz',      'phase':'Degrees'}
        self.mod_base_min =      {'freq':0.5e6,      'phase':0}
        self.mod_base_max =      {'freq':14e6,      'phase':360} 
        self.mod_base_step =     {'freq':5e6,      'phase':10}
        self.mod_base_decimals = {'freq':0,         'phase':0} 
        self.num_DDS = 2
        
        # Create DDS Output objects: we only need frequency for the carrier and frequency and phase for the mod
        dds_prop = {}
        subchnl = 'freq'
        dds_prop['PDH_carrier']={}
        dds_prop['PDH_carrier'][subchnl]={'base_unit':self.carrier_base_units[subchnl],
                                                     'min':self.carrier_base_min[subchnl],
                                                     'max':self.carrier_base_max[subchnl],
                                                     'step':self.carrier_base_step[subchnl],
                                                     'decimals':self.carrier_base_decimals[subchnl]
                                                    }
        subchnl = 'freq'
        dds_prop['PDH_mod']={}
        dds_prop['PDH_mod'][subchnl]={'base_unit':self.mod_base_units[subchnl],
                                                     'min':self.mod_base_min[subchnl],
                                                     'max':self.mod_base_max[subchnl],
                                                     'step':self.mod_base_step[subchnl],
                                                     'decimals':self.mod_base_decimals[subchnl]
                                                    }
        subchnl = 'phase'
        dds_prop['PDH_mod'][subchnl]={'base_unit':self.mod_base_units[subchnl],
                                                     'min':self.mod_base_min[subchnl],
                                                     'max':self.mod_base_max[subchnl],
                                                     'step':self.mod_base_step[subchnl],
                                                     'decimals':self.mod_base_decimals[subchnl]
                                                    }
    #    Create the output objects    
        self.create_dds_outputs(dds_prop)        
        # Create widgets for output objects
        dds_widgets,ao_widgets,do_widgets = self.auto_create_widgets()
        # and auto place the widgets in the UI
        self.auto_place_widgets(("PDH settings",dds_widgets))
        
        connection_object = self.settings['connection_table'].find_by_name(self.device_name)
        connection_table_properties = connection_object.properties
        
        self.TCPIP_port = connection_table_properties.get('TCPIP_port', None)
        self.TCPIP_address = connection_table_properties.get('TCPIP_address', None)
        self.default_TCPIP_port = connection_table_properties.get('default_TCPIP_port', None)
        self.update_mode = connection_table_properties.get('update_mode', 'synchronous')
        
        # Create and set the primary worker
        self.create_worker("main_worker",
                            'labscript_devices.TCPDH_Synth.blacs_workers.TCPDH_SynthWorker',
                            {'TCPIP_port':self.TCPIP_port,
                            'TCPIP_address': self.TCPIP_address,
                            'default_TCPIP_port': self.default_TCPIP_port,
                            'update_mode': self.update_mode})
        
        self.primary_worker = "main_worker"

        # Set the capabilities of this device
        self.supports_remote_value_check(True)
        self.supports_smart_programming(True) 
