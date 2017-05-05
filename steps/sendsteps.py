import numpy as np
import pigpio
import time
pi=pigpio.pi('moby.local')
import numpy_test as nt

periodns=10e6
current_time=np.linspace(0, periodns, num=1000, endpoint=True)
#speed=speed=np.ones_like(current_time)/100000 #100 steps per millisecond
speedparms=[10/1e4,10/1e4]

nsteps=nt.calcsteps(current_time, speedparms)
wave=nt.build_wave(nsteps['stepdelta'])
#print(nsteps)
print len(wave)
print(nsteps['deltap'])

axisen=22

pinstep=12
pindir=6
#pinstep=6
#pindir=12

#pinstep=23
#pindir=24
#pinstep=
pi.set_mode(axisen, pigpio.OUTPUT)
pi.set_mode(pinstep, pigpio.OUTPUT)
pi.set_mode(pindir, pigpio.OUTPUT)
print(pi.read(axisen))
print(pi.read(pindir))
print(pi.read(pinstep))



def astep():
	pi.write(pinstep,1)
	#print(pi.read(pinstep))
	pi.write(pinstep,0)
	#print(pi.read(pinstep))

# pi.write(axisen,0)
# pi.write(pindir,1)
# pi.write(pindir,0)
# pi.write(pinstep,0)
# pi.write(pinstep,1)
# time.sleep(0.1)
# pi.write(pinstep,0)
# pi.write(pinstep,1)
# time.sleep(0.1)
# pi.write(pinstep,0)
# pi.write(pinstep,1)
# time.sleep(0.1)
# pi.write(pinstep,0)
# pi.write(pinstep,1)
# time.sleep(0.1)
# pi.write(pinstep,0)
# pi.write(pinstep,1)
pi.write(axisen,0)
if False:
	for n in range(150):
		astep()
pi.wave_clear()
pi.wave_add_generic(wave)
wid=pi.wave_create()

print(wid)
print("constants are")
print(pigpio.WAVE_MODE_ONE_SHOT_SYNC)
print(dir(pigpio))
for x in range(10):
	pi.wave_send_once(wid)

	#pi.wave_send_once(wid)
	#pi.wave_send_once(wid)
#pi.wave_send_using_mode(wid, pigpio.WAVE_MODE_ONE_SHOT_SYNC)
while pi.wave_tx_busy():
    print(pi.wave_tx_at())
    time.sleep(.1)
pi.write(axisen,1)


