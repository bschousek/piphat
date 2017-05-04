import numpy as np
import cProfile
import pigpio
pi=pigpio.pi('moby.local')

periodns=1e6
current_time=np.linspace(0, periodns, num=1000, endpoint=True)
speed=speed=np.ones_like(current_time)/100000 #100 steps per millisecond
	
def find_steps(current_time, steps):
	last_step=steps[0]
	#print last_step
	for t,step in zip(current_time,steps):
		if step-last_step>=1:
			print t, step, last_step, step-last_step
			
			yield t
		last_step=step
def calcsteps(current_time=current_time, speed=speed):
	speed=np.ones_like(current_time)/100000 #100 steps per millisecond
	#table=np.matrix([current_time, speed])
	expected=np.multiply(current_time,speed)
	#expected2=np.multiply(current_time,speed)
	#print(expected2-expected)
	steps=np.floor(expected)
	steplocs=[step for step in find_steps(current_time, steps)]
	return steplocs
	#return steps, current_time
def multirun():
	for x in range(1000):
		calcsteps()
		get_steps(current_time, steps)
#steps, current_time=calcsteps()



#cProfile.run('multirun()')
sf=calcsteps(current_time, speed)
print sf
print(type(sf))
sss=[s for s in sf]
print(len(sss))


def build_wave():
	wave=[]
	for step in sss:
		p=step
		wave.append(pigpio.pulse(1<<6,0,5))
		wave.append(pigpio.pulse(0,1<<6,10))
		wave.append(pigpio.pulse(0,1<<6,10+p))
	return wave

wave=build_wave()
print(len(wave))

print(wave)
    