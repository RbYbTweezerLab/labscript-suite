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

class TCPDH_SynthAmpConversion(UnitConversion):
    # This must be defined outside of init, and must match the default hardware unit specified within the BLACS tab
    base_unit = 'Arb'
    
    def __init__(self,calibration_parameters = None):            
        self.parameters = calibration_parameters
        
        if hasattr(self,'derived_units'):
            self.derived_units.append('hardware')
        else:
            self.derived_units = ['hardware']        
        
        UnitConversion.__init__(self,self.parameters)

    def hardware_to_base(self,hardware):
        arb = hardware/1023.0
        return arb
    def hardware_from_base(self,arb):
        hardware = arb*1023.0
        return hardware
    
