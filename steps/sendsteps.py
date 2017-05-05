import numpy as np
import pigpio
pi=pigpio.pi('moby.local')
import numpy_test as nt

periodns=5e6
current_time=np.linspace(0, periodns, num=100, endpoint=True)
#speed=speed=np.ones_like(current_time)/100000 #100 steps per millisecond
speedparms=[.1e-5,.1e-5]

nsteps=nt.calcsteps(current_time, speedparms)

print nsteps


pi.set_mode(22, pigpio.OUTPUT)
pi.write(22, 0)


