from __future__ import division
from math import floor
import numpy as np
import cProfile
import logging
logging.basicConfig(filename='csteps.log', filemode='a', level=logging.DEBUG)
import pigpio
#pi=pigpio.pi('moby.local')

periodns=1e6
current_time=np.linspace(0, periodns, num=100, endpoint=True)
#speed=speed=np.ones_like(current_time)/100000 #100 steps per millisecond
speedparms=[1,1]
speed=500
    

def calcsteps(periodns, speed):
    #speed units in steps per second
    #period in units of microseconds per step
    logging.debug('calcsteps periodns is %f speed is %f' %(periodns, speed))
    period=abs(floor(1000000/speed*1000))
    #period=1000000/speed*1000
    logging.debug("calcsteps period is %i" %period)
    steps=floor(periodns/period)
    stepdir=speed>=0
    logging.debug("stepcount %i stepdir %i" %(steps, stepdir))
    return {'period':period,
        'steps':steps,
        'stepdir':stepdir}

def build_wave(steps, dirpin, steppin):
    logging.debug('build_wave dirpin:%i steppin:%i' %(dirpin, steppin))
    wave=[]
    wave.append(pigpio.pulse(1<<dirpin,0,0) if steps['stepdir'] else pigpio.pulse(0,1<<dirpin,0))
    logging.debug('build wave 1 %r' %wave)
    for step in range(int(steps['steps'])):
        wave=wave+[pigpio.pulse(0,1<<steppin,1), pigpio.pulse(0,1<<steppin,5), pigpio.pulse(1<<steppin,0,steps['period'])]
    return wave
    wave=[dipulse]
    
    #steppulse=pigpio.pulse()
    #wave.append(steppulse)
    for step in steps:
        p=int(step/1000)
        wave.append(pigpio.pulse(1<<12,0,5))
        #wave.append(pigpio.pulse(0,1<<12,10))
        wave.append(pigpio.pulse(0,1<<12,10+p))
    return wave

def multirun(n=1000):
    for x in range(n):
        sf=calcsteps(periodns, 100)
        wave=build_wave(sf, 6, 12)
        #get_steps(current_time, steps)
    # print (sf)
    # print(wave)
#steps, current_time=calcsteps()


if __name__ == "__main__":
    prof=True
    if prof:
        cProfile.run('multirun(1000)')
    else:
        sf=calcsteps(periodns, speed)
        print(sf)
        waves=build_wave(sf,6,12)
        print(waves)
        print sf
        print(type(sf))
        sss=[s for s in sf]
        print(len(sss))



#wave=build_wave()
#print(len(wave))

#print(wave)
    