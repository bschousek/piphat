#!/usr/bin/python
import hal
import time
import logging
logging.basicConfig(filename='passthrough.log', level=logging.DEBUG)
#logger=logging.getLogger()
h = hal.component("passthrough")
h.newpin("xvel-cmd", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("xpos-cmd", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("xpos-fb", hal.HAL_FLOAT, hal.HAL_OUT)
h.ready()
xwas = 0
try:
    while 1:
        time.sleep(.01)
        if xwas != h['xpos-cmd']:
        	print("xcmd %f xfb %f xvel %f" %(h['xpos-cmd'], h['xpos-fb'], h['xvel-cmd']))
        	xwas=h['xpos-cmd']
        	h['xpos-fb'] = h['xpos-cmd']

        #logging.info('out %r in %r' %(h['out'], h['in']))
except KeyboardInterrupt:
    raise SystemExit