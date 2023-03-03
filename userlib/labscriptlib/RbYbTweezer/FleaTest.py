from labscript import *

from labscript_utils import import_or_reload
# from labscriptlib.common.functions import *

import_or_reload('labscriptlib.RbYbTweezer.connection_table')

################################################################################
#   Constant Parameters
################################################################################
s, ms, us, ns = 1.0, 1e-3, 1e-6, 1e-9

start()
t = 0
flea2_trigger.go_low(t)
t += 0.1
for i in range(3):
    Flea2_FW.expose(t, name='images', frametype='probe_1', trigger_duration=100*us)
    t += 200*us
    RbImgProbe.go_high(t)
    t += 20*us

    RbImgProbe.go_low(t)
    t += 300*ms

flea2_trigger.go_low(t)
t+=0.1
stop(t)