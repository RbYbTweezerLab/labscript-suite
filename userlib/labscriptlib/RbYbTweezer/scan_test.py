from labscript import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbYbTweezer.connection_table')

Modulation.setfreq(PDH_mod_freq)
Modulation.setphase(28)

start()

t = 0

Carrier.set_freq(t,ramp_start)

t += 100e-6

# oscilloscope_trigger.go_high(t)
# Carrier.set_freq(t,ramp_start + delta_f)

t += 200e-6

Carrier.set_freq(t,ramp_start)

for i in range(0,2):

    Carrier.ramp(t, fc_ramp_time, ramp_start,ramp_stop, n_steps/fc_ramp_time)

    # oscilloscope_trigger.go_low(t)

    t += fc_ramp_time

    Carrier.ramp(t, fc_ramp_time, ramp_stop, ramp_start, n_steps/fc_ramp_time)

    t += fc_ramp_time

t += fc_ramp_time/n_steps

# oscilloscope_trigger.go_low(t)

# Modulation.setphase(28)
Carrier.set_freq(t,ramp_start)

stop(t)