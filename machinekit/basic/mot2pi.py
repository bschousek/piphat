#!/usr/bin/python
import hal
import time
import logging
import sys
sys.path.append('/home/vagrant/Documents/piphat/steps')
print(sys.path)
import motor_wave as mw
import pigpio

pi=pigpio.pi('moby.local')
xaxis=mw.Motor(pinstep=12, pindir=6, axisen=22, periodns=10000000, axis_id='X', pi=pi)
xaxis.enable()
yaxis=mw.Motor(pinstep=24, pindir=23, axisen=22, periodns=10000000, axis_id='Y', pi=pi)
yaxis.enable()

logging.basicConfig(filename='mot2pi.log', level=logging.DEBUG)
#logger=logging.getLogger()
h = hal.component("mot2pi")
h.newpin("xvel-cmd", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("xpos-cmd", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("xpos-fb", hal.HAL_FLOAT, hal.HAL_OUT)

h.newpin("yvel-cmd", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("ypos-cmd", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("ypos-fb", hal.HAL_FLOAT, hal.HAL_OUT)
#h.newpin("zvel-cmd", hal.HAL_FLOAT, hal.HAL_IN)
#h.newpin("zpos-cmd", hal.HAL_FLOAT, hal.HAL_IN)
#h.newpin("zpos-fb", hal.HAL_FLOAT, hal.HAL_OUT)
h.ready()
poswas = [0,0]
posnow=[None, None]
logging.debug("poswas %r posnow %r" %(poswas, posnow))
try:
    while 1:
        time.sleep(.01)
        posnow=[h['xpos-cmd'], h['ypos-cmd']]
        if poswas != posnow:
        	logging.debug("poswas %r posnow %r" %(poswas, posnow))
        	s1=("xcmd %f xfb %f xvel %f" %(h['xpos-cmd'], h['xpos-fb'], h['xvel-cmd']))
        	s2=("ycmd %f yfb %f yvel %f" %(h['ypos-cmd'], h['ypos-fb'], h['yvel-cmd']))
        	print(s1, s2)
        	poswas=posnow
        	h['xpos-fb'] = h['xpos-cmd']
        	h['ypos-fb'] = h['ypos-cmd']
        	xwave=xaxis.make_wave(h['xvel-cmd']*1000*10)
        	ywave=yaxis.make_wave(h['yvel-cmd']*1000*10)
    		pi.wave_clear()
        
	        pi.wave_add_generic(xwave)
	        pi.wave_add_generic(ywave)
	        wid=pi.wave_create()
	        pi.wave_send_once(wid)

        #logging.info('out %r in %r' %(h['out'], h['in']))
except KeyboardInterrupt:
    xaxis.disable()
    raise SystemExit