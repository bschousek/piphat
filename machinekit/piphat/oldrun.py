#!/usr/bin/python
import logging
format='%(asctime)s %(module)s %(funcName)s %(lineno)s %(message)s'
logging.basicConfig(filename='voron.log',level=logging.DEBUG,format=format)
import sys
import os
import subprocess
import time
from machinekit import launcher


launcher.register_exit_handler()
launcher.set_debug_level(5)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    launcher.check_installation()
    launcher.cleanup_session()
    
    #launcher.ensure_mklauncher()  # ensure mklauncher is started
    #launcher.start_realtime()  # start Machinekit realtime environment
    #launcher.ensure_mklauncher()  # ensure mklauncher is started
    #launcher.load_bbio_file('cramps2_cape.bbio')
    logging.debug("starting machineface")
    launcher.start_process("configserver -d -n voron ~/Machineface/ ~/Cetus/")
    #launcher.start_realtime()  # start Machinekit realtime environment
    logging.debug("starting machinekit piphat.ini")
    launcher.start_process('linuxcnc piphat.ini')
    #launcher.load_hal_file('voron.py')  # load the main HAL file
    #launcher.start_process('machinekit piphat.ini')
    logging.debug("piphat.ini started")
    launcher.register_exit_handler()  # enable on ctrl-C, needs to executed after HAL files

    while True:
        launcher.check_processes()
        time.sleep(1)
except (subprocess.CalledProcessError, KeyboardInterrupt):
    logging.debug("subprocess called error or keyboard")
    launcher.end_session()
    launcher.cleanup_session()
    sys.exit(1)

sys.exit(0)
    