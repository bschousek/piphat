# HAL file for Raspberry Pi + piphat with 5 steppers
import os
import logging
format='%(asctime)s %(module)s %(funcName)s %(lineno)s %(message)s'
logging.basicConfig(filename='voron.log',level=logging.DEBUG,format=format)

from machinekit import rtapi as rt
from machinekit import hal
from machinekit import config as c

from fdm.config import velocity_extrusion as ve
from fdm.config import base
from fdm.config import storage
from fdm.config import motion
def check_axis(n=0):
    str=filter(lambda x:'axis.0.joint' in x,hal.pins())
    logging.debug("acheck %i %r" %(n, str))
check_axis(1)

import piphat as hardware
check_axis(2)

# initialize the RTAPI command client
logging.debug("starting rtapi")
rt.init_RTAPI()
logging.debug("rtapi should be started")
#logging.debug('rt now is %r' %(dir(rt)))
# loads the ini file passed by linuxcnc
#logging.debug('os environment  is %r' %os.environ)
c.load_ini(os.environ['INI_FILE_NAME'])
check_axis(3)

logging.debug("starting motion")
#motion.setup_motion(kinematics="corexykins")
motion.setup_motion()
check_axis(4)
logging.debug("motion should be started")
hardware.init_hardware()
check_axis(5)
logging.debug("done init")
storage.init_storage('storage.ini')

# reading functions
hw=True
if hw:
    hardware.hardware_read()
hal.addf('motion-command-handler', 'servo-thread')
hal.addf('motion-controller', 'servo-thread')
hal.addf('hps.funct', 'servo-thread')

numFans = c.find('FDM', 'NUM_FANS')
numExtruders = c.find('FDM', 'NUM_EXTRUDERS')
numLights = c.find('FDM', 'NUM_LIGHTS')
logging.debug("fans %i extruders %i lights %i" %(numFans, numExtruders, numLights))
#raw_input()
# Axis-of-motion Specific Configs (not the GUI)
ve.velocity_extrusion(extruders=numExtruders, thread='servo-thread')
# X [0] Axis
#base.setup_stepper(section='AXIS_0', stepgenType= 'hps',axisIndex=0, velocitySignal=hal.pins['axis.0.joint-vel-cmd'], stepgenIndex=0, thread='servo-thread')
base.setup_stepper(section='AXIS_0', stepgenType= 'hps',axisIndex=0, stepgenIndex=0, thread='servo-thread')

# Y [1] Axis
base.setup_stepper(section='AXIS_1', stepgenType= 'hps',axisIndex=1, stepgenIndex=1, thread='servo-thread')
# Z [2] Axis
base.setup_stepper(section='AXIS_2', stepgenType= 'hps',axisIndex=2, stepgenIndex=2, thread='servo-thread')
# Extruder, velocity controlled
for i in range(0, numExtruders):
    base.setup_stepper(section='EXTRUDER_%i' % i, stepgenType= 'hps', stepgenIndex=3,
                       velocitySignal='ve-extrude-vel', thread='servo-thread')

# Extruder Multiplexer
base.setup_extruder_multiplexer(extruders=numExtruders, thread='servo-thread')

# Stepper Multiplexer
multiplexSections = []
for i in range(0, numExtruders):
    multiplexSections.append('EXTRUDER_%i' % i)
base.setup_stepper_multiplexer(stepgenIndex=4, sections=multiplexSections,
                               selSignal='extruder-sel', thread='servo-thread')

# Fans
for i in range(0, numFans):
    base.setup_fan('f%i' % i, thread='servo-thread')

# Temperature Signals
# base.create_temperature_control(name='hbp', section='HBP',
#                                 hardwareOkSignal='temp-hw-ok',
#                                 thread='servo-thread')
for i in range(0, numExtruders):
    base.create_temperature_control(name='e%i' % i, section='EXTRUDER_%i' % i,
                                    coolingFan='f%i' % i,
                                    hardwareOkSignal='temp-hw-ok',
                                    thread='servo-thread')

# LEDs
for i in range(0, numLights):
    base.setup_light('l%i' % i, thread='servo-thread')

# Standard I/O - EStop, Enables, Limit Switches, Etc
#errorSignals = ['temp-hw-error', 'watchdog-error', 'hbp-error']
errorSignals = []
logging.debug("errorsignals are %r" %errorSignals)
#for i in range(0, numExtruders):
#    errorSignals.append('e%i-error' % i)
logging.debug("setting up estop")
base.setup_estop(errorSignals, thread='servo-thread')
logging.debug("setting up tool loopback")
base.setup_tool_loopback()
# Probe
base.setup_probe(thread='servo-thread')
# Setup Hardware
hardware.setup_hardware(thread='servo-thread')

# write out functions
hardware.hardware_write()

# Storage
storage.read_storage()

# start haltalk server after everything is initialized
# else binding the remote components on the UI might fail
logging.debug("starting server")
hal.loadusr('haltalk', wait=True)
logging.debug("server should  be started")
