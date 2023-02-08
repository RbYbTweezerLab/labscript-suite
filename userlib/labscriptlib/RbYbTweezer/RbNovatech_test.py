from labscript import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbYbTweezer.connection_table')




start()
t = 0
Rb_cooling_F.setamp(t,value=0.9,units=None)
Rb_repump_F.setamp(t,value=0.7,units=None)
t += 3

Dev1_DO0.go_high(t)
Rb_cooling_F.setfreq(t,value=86e6,units=None)
Rb_repump_F.setfreq(t,value=RbrepumpJumpF,units=None)
# Rigol_CH2_trigger.go_low(t)

t += 30

Rb_cooling_F.setfreq(t,value=89e6,units=None)
Rb_repump_F.setfreq(t,value=RbrepumpF0,units=None)
t += 0.1
Rb_cooling_F.setamp(t,value=0.9,units=None)
Rb_repump_F.setamp(t,value=0.7,units=None)
stop(t)