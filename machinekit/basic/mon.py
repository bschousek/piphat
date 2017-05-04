from machinekit import hal
import time

pins=hal.pins
jpos =pins['axis.0.joint-pos-cmd']
xpos =pins['axis.0.motor-pos-cmd']
xvel=pins['axis.0.joint-vel-cmd']
xwas=xpos.get()
twas=0
while(True):
	xnow=xpos.get()
	if xnow != xwas:

		tnow=time.clock()*1e6
		tdelta=tnow-twas
		print ("%i %i %f %f %f" %(tnow, tdelta, xnow, xvel.get(), jpos.get()))
		xwas=xnow
		twas=tnow
