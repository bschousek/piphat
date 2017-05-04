import hal, time
import pigpio

class Pihal(object):
	
	def __init__(self, pi, version, pins, h):
		self.inputs=list()
		self.outputs=list()
		self.piphat_version=version
		self.pi=pi
		self.h=h

		pud_type={'PUD_OFF':pigpio.PUD_OFF,
			'PUD_UP':pigpio.PUD_UP,
			'PUD_DOWN':pigpio.PUD_DOWN}

		for line in pins:
			gpio, direction, name, value=line
			print(direction)
			if direction=='in':
				pi.set_pull_up_down(gpio, pud_type[value])
				pi.set_mode(gpio, pigpio.INPUT)
				h.newpin(name, hal.HAL_BIT, hal.HAL_OUT)
				self.inputs.append(line)
			elif direction=='out':
				pi.write(gpio, 0 if value=='low' else 1)
				pi.set_mode(gpio, pigpio.OUTPUT)
				h.newpin(name, hal.HAL_BIT, hal.HAL_IN)
				self.outputs.append(line)
			else:
				raise Exception

	def update(self):
		for line in self.inputs:
			gpio, direction, name, value=line
			self.h[name]=self.pi.read(gpio)
		for line in self.outputs:
			gpio, direction, name, value=line
			self.pi.write(gpio, self.h[name])


pi=pigpio.pi('moby.local')
h = hal.component("pigpio")
from piphat_pigpio import piphat_version, piphat_pins
ph=Pihal(pi, piphat_version, piphat_pins, h)
print (ph.inputs)
print(ph.outputs)


h.ready()
try:
    while 1:
        time.sleep(1)
        ph.update()
        #h['out'] = h['in']
except KeyboardInterrupt:
    raise SystemExit
finally:
	print("must have closed halcmd")


