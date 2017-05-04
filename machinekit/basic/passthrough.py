#!/usr/bin/python
import hal
import time
import logging
logging.basicConfig(filename='passthrough.log', level=logging.DEBUG)
#logger=logging.getLogger()
h = hal.component("passthrough")
h.newpin("in", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("out", hal.HAL_FLOAT, hal.HAL_OUT)
h.ready()
try:
    while 1:
        time.sleep(.01)
        h['out'] = h['in']
        #logging.info('out %r in %r' %(h['out'], h['in']))
except KeyboardInterrupt:
    raise SystemExit