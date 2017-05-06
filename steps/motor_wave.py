from __future__ import division
from math import floor
import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
from time import sleep
import pigpio
#pi=pigpio.pi()
import numpy as np
#logger=logging.getLogger()

class Motor:

    def __init__(self, pinstep, pindir, axisen, periodns, axis_id, pi, position=0):
        self.position = position
        self.pinstep = pinstep
        self.pindir = pindir
        self.axis_id = axis_id
        self.axisen = axisen
        self.periodns = periodns
        self.pi=pi


    def forcepins(self, level=0):
        pi=self.pi
        pi.set_mode(self.pinstep, pigpio.OUTPUT)
        pi.set_mode(self.pindir, pigpio.OUTPUT)
        pi.set_mode(self.axisen, pigpio.OUTPUT)
        pi.write(self.pinstep, level)
        pi.write(self.pindir, level)
        pi.write(self.axisen, level)
    def enable(self):
        self.forcepins(0)
    def disable(self):
        self.forcepins(1)



    #def calcsteps(self, velocity):

    def make_wave(self, velocity):
        logging.debug('calcsteps periodns is %f speed is %f' %(self.periodns, velocity))
        #velocity is in steps per second
        #periodns is in units of nanoseconds (for Machinekit)
        #We need to calculate step interval in microseconds (for pigpio)
        
        # So Step interval is 1/velocity (steps/second) * 1e6(microseconds/second)
        step_interval=abs(floor(1e6/velocity))
        logging.debug("step interval is %i" %step_interval)
        # Number of steps that will fit in periodns is periodns (ns) * (1000 us/ns) / step_interval (us/step)
        step_count=floor(self.periodns/1000/step_interval)
        logging.debug("step count is %i" %step_count)
        stepdir=velocity>=0
        logging.debug("direction is %i" %stepdir)

        pindir=self.pindir
        pinstep=self.pinstep
        logging.debug('building wave dirpin:%i steppin:%i' %(pindir, pinstep))
        dirhold=5
        stephold=5
        wave=[]
        wave.append(pigpio.pulse(1<<pindir,0,0) if stepdir else pigpio.pulse(0,1<<pindir,0))
        #wave.append(0,0,dirhold)
        for step in range(int(step_count)):
            wave=wave+[pigpio.pulse(0,1<<pinstep,0),
             pigpio.pulse(0,1<<pinstep,stephold),
             pigpio.pulse(1<<pinstep,0,step_interval-stephold)]
        return wave
        





if __name__ == '__main__':
    # path=[
    # [500,0,1e5],
    # [1000,0,1e5],
    # [1500,0,1e5],
    # ]
    # #[50,0,1e5],
    #[50,50,1e5],
    #[0,0,1e5]
    #]
    #pi.set_mode
    pi=pigpio.pi('moby.local')
    xaxis=Motor(pinstep=12, pindir=6, axisen=22, periodns=1000000, axis_id='X', pi=pi)
    yaxis=Motor(pinstep=24, pindir=23, axisen=22, periodns=1000000, axis_id='Y', pi=pi)
    xwave=xaxis.make_wave(10000)
    ywave=yaxis.make_wave(-10000)


    runx=True
    if runx:
        pi.wave_clear()
        
        pi.wave_add_generic(xwave)
        wid=pi.wave_create()
        xaxis.enable()
        if True:
            for x in range(200):
                pi.wave_send_once(wid)
        while pi.wave_tx_busy():
            print(pi.wave_tx_at())
            time.sleep(.1)

        xaxis.disable()
    runy=True
    if runy:
        pi.wave_clear()
        
        pi.wave_add_generic(ywave)
        wid=pi.wave_create()
        yaxis.enable()
        if True:
            for x in range(200):
                pi.wave_send_once(wid)
        while pi.wave_tx_busy():
            print(pi.wave_tx_at())
            time.sleep(.1)

        yaxis.disable()
    runboth=True
    if runboth:
        pi.wave_clear()
        pi.wave_add_generic(xwave)
        pi.wave_add_generic(ywave)
        wid=pi.wave_create()
        xaxis.enable()
        yaxis.enable()
        for x in range(200):
                pi.wave_send_once(wid)
        while pi.wave_tx_busy():
            print(pi.wave_tx_at())
            time.sleep(.1)

        xaxis.disable()
        yaxis.disable()

    # for line in path:
    #     logging.info("this line is %r" %line)
    #     new_wave=xaxis.goto(newposition=line[0], tdelta=line[2])
    #     pi.wave_add_generic(new_wave)
    #     new_wave2=yaxis.goto(newposition=line[1], tdelta=line[2])
    #     pi.wave_add_generic(new_wave2)
        
    #     wlist.append(pi.wave_create())

    # cbs = pi.wave_get_cbs()
    # logging.info("cbs is %r" %cbs)
    # max_cbs=pi.wave_get_max_cbs()
    # logging.info("max cbs is %r" %max_cbs)

    # pulses = pi.wave_get_max_pulses()
    # logging.info("max pulses is %r" %pulses)
    # logging.info("type of wlist is %r" %(type(wlist)))

    # logging.info("current wf is %r us" %pi.wave_get_micros())
    # logging.info("current wf has %r pulses" %pi.wave_get_pulses())
    # #print(wlist)
    # pi.set_mode(22, pigpio.OUTPUT)
    # pi.write(22, 0)
    # a=pi.wave_chain(wlist)
    # print(a)
    # while pi.wave_tx_busy():
    # #    print(1)
    #     sleep(0.1)
    #for i in wlist:
    #    pi.wave_delete(i)


                





