import hal, time
import pigpio
from piphat_pigpio import piphat_version, piphat_pins
pi=pigpio.pi('moby.local')
h = hal.component("pigpio")
print(piphat_version)

pinlist=dict()
pvalue={'PUD_OFF':pigpio.PUD_OFF,
'PUD_UP':pigpio.PUD_UP,
'PUD_DOWN':pigpio.PUD_DOWN,
'low':0,
'high':1}


for line in piphat_pins:
	pin, direction, name, value=line
	if direction=='in':
		pi.set_pull_up_down(pin, pud_type[pullup])
		h.newpin(name, hal.HAL_BIT, hal.HAL_OUT)
	elif direction=='out':
		pass
	else:
		raise Exception
	pi.write(pin, pin_level[direction])	
	pi.set_mode(pin, pin_mode[direction])
	h.newpin(name, hal.HAL_BIT, hal_mode[direction])


h.ready()
try:
    while 1:
        time.sleep(1)
        #h['out'] = h['in']
except KeyboardInterrupt:
    raise SystemExit
finally:
	print("must have closed halcmd")
