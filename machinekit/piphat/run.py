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
launcher.set_debug_level(3)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    logging.debug("check installation")
    launcher.check_installation()
    logging.debug("cleanup session")
    launcher.cleanup_session()
    logging.debug("make launcher")
    launcher.ensure_mklauncher()  # ensure mklauncher is started
    logging.debug("config server")
    launcher.start_process("configserver -d -n QQVsim ~/Machineface/")
    logging.debug("start piphat")
    launcher.start_process('linuxcnc piphat.ini')
    logging.debug("check_processes")
    launcher.check_processes()
    logging.debug("now loop")
    
    while True:
        launcher.check_processes()
        time.sleep(1)

except subprocess.CalledProcessError:
    logging.debug("end process")
    launcher.end_session()
    sys.exit(1)

sys.exit(0)
