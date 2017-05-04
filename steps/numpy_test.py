import numpy as np
import cProfile
import logging
logging.basicConfig(filename='csteps.log', filemode='a', level=logging.INFO)
import pigpio
#pi=pigpio.pi('moby.local')

periodns=1e6
current_time=np.linspace(0, periodns, num=100, endpoint=True)
#speed=speed=np.ones_like(current_time)/100000 #100 steps per millisecond
speedparms=[0e-5,1e-5]
    
def find_steps(current_time, steps):
    
    last_step=steps[0]
    #print last_step
    for t,step in zip(current_time,steps):
        logging.debug
        if abs(step-last_step)>=1:
            #print n, t, step, last_step, step-last_step
            n,=np.where(current_time==t)
            #print(n)
            #print(n)
            yield n[0]
        last_step=step
def sfind_steps(current_time, steps):
#     pets=current_time-steps
#     print(steps)
#     print(current_time)
#     print("pets")
#     print(pets)
    last_step=steps[0]
    for step in steps:
        #print(step)
        if step>last_step:
            n,=np.where(steps==step)
        
            #print(n)
        #print(n)
            yield n[0]
        last_step=step
#     last_step=steps[0]
#     #print last_step
#     for t,step in zip(current_time,steps):
#         logging.debug
#         if abs(step-last_step)>=1:
#             #print n, t, step, last_step, step-last_step
#             n,=np.where(current_time==t)
#             #print(n)
#             #print(n)
#             yield n[0]
#         last_step=step
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
    if full:
        retval={'steplocs':steplocs,
                'steptimes':current_time[steplocs],
                'speeds': speed[steplocs]}
        retval['stepdir']=retval['speeds']>0
        #print 
        retval['stepdelta']=np.diff(np.insert(retval['steptimes'],0,0))
        retval['stepcount']=len(steplocs)
        retval['deltap']=np.sum(retval['stepdir'])- np.sum(np.invert(retval['stepdir']))
    else:
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
        p=step
        wave.append(pigpio.pulse(1<<6,0,5))
        wave.append(pigpio.pulse(0,1<<6,10))
        wave.append(pigpio.pulse(0,1<<6,10+p))
    return wave

def multirun(n=1000):
     for x in range(n):
         sf=calcsteps()
         build_wave(sf['stepdelta'])
         #get_steps(current_time, steps)
#steps, current_time=calcsteps()


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
    