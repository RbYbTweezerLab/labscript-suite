from labscript import *

from labscript_utils import import_or_reload
# from labscriptlib.common.functions import *

import_or_reload('labscriptlib.RbYbTweezer.connection_table')

################################################################################
#   Constant Parameters
################################################################################
s, ms, us, ns = 1.0, 1e-3, 1e-6, 1e-9

SRS_shutter_open_time=0
SRS_shutter_close_time=0


Modulation.setfreq(TCPDH_fmod)

start()
t = 0

################################################################################
#   Step 1: Initalize 
################################################################################
flea2_trigger.go_low(t)
andor_camera_trigger.go_low(t)
flea3_trigger.go_low(t)
cooling_shutter.go_high(t)
cooling_aom_ttl.disable(t)      
oscilloscope_trigger.go_low(t)
Rigol_CH2_trigger.go_low(t)

NT2_1.setamp(t,value=0.0,units=None)
NT2_1.setfreq(t,value=96e6,units=None)
NT2_1.setphase(t,value=0,units=None)

Carrier.set_freq(t,f_start)

t += 0.25

################################################################################
#   Step 1: Initalize 
################################################################################

for i in range(0,1):
    Carrier.ramp(t, ramp_time, f_start, f_stop, n_steps/ramp_time)
    t += ramp_time

    Carrier.ramp(t, ramp_time, f_stop, f_start, n_steps/ramp_time)
    t += ramp_time


################################################################################
#   Step n: 
################################################################################
flea2_trigger.go_low(t)
andor_camera_trigger.go_low(t)
flea3_trigger.go_low(t)
cooling_shutter.go_high(t)
cooling_aom_ttl.disable(t)      
oscilloscope_trigger.go_low(t)
Rigol_CH2_trigger.go_low(t)

NT2_1.setamp(t,value=0.0,units=None)
NT2_1.setfreq(t,value=96e6,units=None)
NT2_1.setphase(t,value=0,units=None)

Carrier.set_freq(t,f_start)

stop(t)