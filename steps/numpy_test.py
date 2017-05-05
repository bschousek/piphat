import numpy as np
import cProfile
import logging
logging.basicConfig(filename='csteps.log', filemode='a', level=logging.INFO)
import pigpio
#pi=pigpio.pi('moby.local')

periodns=1e6
current_time=np.linspace(0, periodns, num=100, endpoint=True)
#speed=speed=np.ones_like(current_time)/100000 #100 steps per millisecond
speedparms=[1,1]
    

def calcsteps(current_time=current_time, speedparms=speedparms):
    speed=np.linspace(speedparms[0], speedparms[1], len(current_time))
    expected=np.multiply(current_time,speed)
    steps=np.diff(np.floor(expected))
    steplocs=np.where(steps !=0)[0]
    steptimes=current_time[steplocs]
    stepdelta=np.diff(np.insert(steptimes,0,0))
    stepdir=speed[steplocs]>0
    deltap=np.sum(stepdir)-np.sum(np.invert(stepdir))
    full=False

    retval={'steplocs':steplocs,
            'steptimes':current_time[steplocs],
            'speeds': speed[steplocs],
            'stepdelta': stepdelta,
            'stepdir':stepdir,
            'deltap': deltap}
        #logging.debug('steplocs %r' %steplocs)
    #logging.debug('steptimes %r' %current_time[steplocs])
    #logging.debug('speeds %r' %speed[steplocs])
    
    #logging.debug('retval %r' %retval)
    return retval
    #return steps, current_time
def build_wave(steps):
    wave=[]
    for step in steps:
        p=int(step/1000)
        wave.append(pigpio.pulse(1<<12,0,5))
        #wave.append(pigpio.pulse(0,1<<12,10))
        wave.append(pigpio.pulse(0,1<<12,10+p))
    return wave

def multirun(n=1000):
     for x in range(n):
         sf=calcsteps()
         build_wave(sf['stepdelta'])
         #get_steps(current_time, steps)
#steps, current_time=calcsteps()


if __name__ == "__main__":
    prof=True
    if prof:
        cProfile.run('multirun(1000)')
    else:
        sf=calcsteps(current_time, speedparms)
        waves=build_wave(sf['stepdelta'])
        print(waves)
        print sf
        print(type(sf))
        sss=[s for s in sf]
        print(len(sss))



#wave=build_wave()
#print(len(wave))

#print(wave)
    