#####################################################################
#                                                                   #
# generic_frequency.py                                              #
#                                                                   #
# Copyright 2022, Monash University and contributors                #
#                                                                   #
# This file is part of the labscript suite (see                     #
# http://labscriptsuite.org) and is licensed under the Simplified   #
# BSD License. See the license.txt file in the root of the project  #
# for the full license.                                             #
#                                                                   #
#####################################################################
"""Generic frequency conversion"""

from .UnitConversionBase import *

class TCPDH_SynthPhaseConversion(UnitConversion):
    # This must be defined outside of init, and must match the default hardware unit specified within the BLACS tab
    base_unit = 'Degrees'
    
    def __init__(self,calibration_parameters = None):            
        self.parameters = calibration_parameters
        
        if hasattr(self,'derived_units'):
            self.derived_units.append('hardware')
        else:
            self.derived_units = ['hardware']        
        
        UnitConversion.__init__(self,self.parameters)

    def hardware_to_base(self,hardware):
        return hardware
    def hardware_from_base(self,base):
        return base