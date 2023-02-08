from labscript import *

from labscript_utils import import_or_reload
# from labscriptlib.common.functions import *

import_or_reload('labscriptlib.RbYbTweezer.connection_table')


################################################################################
#   Constant Parameters
################################################################################

SRS_shutter_open_time=0
SRS_shutter_close_time=0

################################################################################
#   Initialize
################################################################################


start()
t=0
t+=2
Flea2_FW.expose(t,name='abs_image', frametype='atoms', trigger_duration=exptime_flea)
# Andor_iXon_ultra.expose(t,name='test', frametype='frame_1', trigger_duration=100e-6)

t+=500e-3
Flea2_FW.expose(t,name='abs_image', frametype='probe', trigger_duration=exptime_flea)
# Andor_iXon_ultra.expose(t,name='test', frametype='frame_2', trigger_duration=25e-6)

t+=500e-3
Flea2_FW.expose(t,name='abs_image', frametype='background', trigger_duration=exptime_flea)
# Andor_iXon_ultra.expose(t,name='test', frametype='frame_3', trigger_duration=50e-6)

t+=2
stop(t)
