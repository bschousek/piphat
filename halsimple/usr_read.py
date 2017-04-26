# import hal, time
# h=hal.component("pymotor")
# h.newpin("xpos", hal.HAL_FLOAT, hal.HAL_OUT)
# h.newpin("xvel", hal.HAL_FLOAT, hal.HAL_OUT)
# hal.connect("xpos", "halui.axis.0.pos-feedback")
# hal.net("xvel", "axis.0.joint-vel-cmd")

import linuxcnc
s = linuxcnc.stat()
s.poll()
for i in [0,1,2]:
	print ('Axis %i output: %f' %(i,s.axis[i]['output']))
	print ('Axis %i ferror: %f' %(i,s.axis[i]['ferror_current']))
	print ('Axis %i velocity: %f' %(i,s.axis[i]['velocity']))
