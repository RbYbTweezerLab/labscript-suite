from labscript import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbYbTweezer.connection_table')




start()
t = 0

t==10
Rb_cooling_F.setamp(t,value=0.9,units=None)
Rb_repump_F.setamp(t,value=0.7,units=None)


Rb_cooling_F.setfreq(t,value=86e6,units=None)
Rb_repump_F.setfreq(t,value=RbrepumpJumpF,units=None)
# Rigol_CH2_trigger.go_low(t)

t += 20

Rb_cooling_F.setfreq(t,value=139727000,units=None)
Rb_repump_F.setfreq(t,value=86143900,units=None)

Rb_cooling_F.setamp(t,value=0.9,units=None)
Rb_repump_F.setamp(t,value=0.7,units=None)
stop(t)