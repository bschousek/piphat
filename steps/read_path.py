import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
from time import sleep
import pigpio
#pi=pigpio.pi()
pi=pigpio.pi('moby.local')
import numpy as np
#logger=logging.getLogger()

class Axis:

    def __init__(self, pinstep, pindir, axisen, axis_id, position=0):
        self.position=position
        self.pinstep=pinstep
        self.pindir=pindir
        self.axis_id=axis_id
        self.axisen=axisen
        pi.set_mode(pinstep, pigpio.OUTPUT)
        pi.set_mode(pindir, pigpio.OUTPUT)


    def goto(self, newposition, tdelta=1):
        sdir=newposition-self.position>0
        logging.info ("newgoto %r %i %i %r" %(self.axis_id, newposition, tdelta, sdir))
        steps=np.linspace(0, tdelta, abs(newposition-self.position))
        #pi.wave_clear()
        #logging.info(print (len(steps))
        wave=[]

        if sdir:
            logging.info("forward")
            wave.append(pigpio.pulse(1<<self.pindir,0,int(0)))
        else:
            logging.info("backward")
            wave.append(pigpio.pulse(0,1<<self.pindir,int(0)))

        logging.info("%r steps" %len(steps))
        if newposition != self.position:
            delay=int(tdelta/(abs(newposition-self.position)))
            for s in steps:
                
                p=int(s)
                #logging.info("s %r p %r" %(s,p))
                wave.append(pigpio.pulse(1<<self.pinstep,0,5))
                wave.append(pigpio.pulse(0,1<<self.pinstep,10))
                wave.append(pigpio.pulse(0,1<<self.pinstep,delay-5-10))

        #logging.info("end time %r" %p)
        #logging.info("steps are %r " %steps)
        #pi.wave_add_generic(wave)
        #pi.set_mode(pindir, wave)
        #owave=pi.wave_create()

        self.position=newposition
        logging.info("newposition %r" %newposition)
        return wave



path=[
[500,0,1e5],
[1000,0,1e5],
[1500,0,1e5],
]
#[50,0,1e5],
#[50,50,1e5],
#[0,0,1e5]
#]
#pi.set_mode
xaxis=Axis(pinstep=12, pindir=6, axis_id='X')
yaxis=Axis(pinstep=24, pindir=23, axis_id='Y')
wlist=[]
pi.wave_clear()
for line in path:
    logging.info("this line is %r" %line)
    new_wave=xaxis.goto(newposition=line[0], tdelta=line[2])
    pi.wave_add_generic(new_wave)
    new_wave2=yaxis.goto(newposition=line[1], tdelta=line[2])
    pi.wave_add_generic(new_wave2)
    
    wlist.append(pi.wave_create())

cbs = pi.wave_get_cbs()
logging.info("cbs is %r" %cbs)
max_cbs=pi.wave_get_max_cbs()
logging.info("max cbs is %r" %max_cbs)

pulses = pi.wave_get_max_pulses()
logging.info("max pulses is %r" %pulses)
logging.info("type of wlist is %r" %(type(wlist)))

logging.info("current wf is %r us" %pi.wave_get_micros())
logging.info("current wf has %r pulses" %pi.wave_get_pulses())
#print(wlist)
pi.set_mode(22, pigpio.OUTPUT)
pi.write(22, 0)
a=pi.wave_chain(wlist)
print(a)
while pi.wave_tx_busy():
#    print(1)
    sleep(0.1)
#for i in wlist:
#    pi.wave_delete(i)


            





