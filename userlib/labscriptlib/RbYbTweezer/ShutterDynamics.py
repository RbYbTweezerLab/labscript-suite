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

################################################################################
#   Initialize
################################################################################


start()
t = 0

flea2_trigger.go_low(t)
andor_camera_trigger.go_low(t)
flea2_trigger.go_low(t)
cooling_shutter.go_low(t)
cooling_aom_ttl.go_low(t)      
oscilloscope_trigger.go_low(t)

t += 1

cooling_shutter.go_high(t)

t += 500*ms

Flea2_FW.expose(t,name='images', frametype='probe', trigger_duration=200*us)

t += 100*ms

flea2_trigger.go_low(t)
andor_camera_trigger.go_low(t)
flea2_trigger.go_low(t)
cooling_shutter.go_low(t)
cooling_aom_ttl.go_low(t)      
oscilloscope_trigger.go_low(t)

stop(t)
