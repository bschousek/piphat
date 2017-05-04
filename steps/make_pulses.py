#Python implementation of make_pulses from stepgenv2.c
# user mode only for now

#import linuxcnc
from __future__ import division
import logging
logging.basicConfig(level=logging.DEBUG)


class stepgen(object):

	def __init__(self, periodns, deltalim=1, step_len=5000, dir_hold_dly=5000, dir_setup=5000):
		self.periodns=periodns
		self.deltalim=deltalim
		self.step_len=step_len
		self.dir_hold_dly=dir_hold_dly
		self.dir_setup=dir_setup

		#self.target_addval=0
		#self.curr_dir=1
		self.rawcount=0

		#self.pos_scal=1
		#self.scale_recip=1/self.pos_scal
		self.pos_cmd=0
		#self.old_pos_cmd=0
		self.vel_cmd=0
		self.maxvel=10
		self.maxaccel=10
#		self.deltalim=
		self.enable=False
		self.current_position=0
		self.current_velocity=0

	def make_pulses(self):
		# First figure out what actual delta_v and accel values will be 
		periodns=self.periodns
		delta_v = self.vel_cmd - self.current_velocity
		accel = delta_v / periodns
		logging.debug("calc deltav %f, accel %f" %(delta_v, accel))
		if accel > self.maxaccel:
			accel = self.maxaccel
		delta_v = accel * periodns
		logging.debug("limited deltav %f, accel %f" %(delta_v, accel))
		
		
		#final_v = self.current_velocity+periodns*deltav
		
		steps=[]
		current_time=0
		def f_velocity(t, vstart=self.current_velocity, accel=accel):
			return vstart+accel*t
		while(current_time<periodns):
			velocity=f_velocity(current_time)
			try:
				steplen=1/velocity
			#if velocity starts at zero we need to give it a kick
			except ZeroDivisionError:
				#steplen=0
				logging.debug('zero division at t%f' %current_time)
				#current_time=periodns
				steplen=1/self.vel_cmd
			steps.append(steplen)
			current_time += steplen

			#print(current_time)
		logging.debug("end velocity %f" %(1/steplen))
		logging.debug("stepcount %i" %len(steps))	
		return steps

def test_stepgen():
	axis=stepgen(1000000)
	print(axis)
	axis.vel_cmd=1
	steps=axis.make_pulses()
	print(steps)
	axis.vel_cmd=2
	steps=axis.make_pulses()
	print(steps)





