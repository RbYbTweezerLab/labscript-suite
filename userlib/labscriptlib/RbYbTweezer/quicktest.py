from labscript import *

from labscript_utils import import_or_reload
# from labscriptlib.common.functions import *

import_or_reload('labscriptlib.RbYbTweezer.connection_table')

################################################################################
#   Constant Parameters
################################################################################


start()
t = 0

pb_10.go_high(t)
t+=60
pb_10.go_low(t)
t += 0.1
stop(t)