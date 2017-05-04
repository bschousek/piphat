# you might have to:
# sudo easy_install cmd2 readline
# or the equivalent debian incantations, whatever they are
from cmd2 import Cmd
import linuxcnc

class MachinekitApp(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.c = linuxcnc.command()
        self.s = linuxcnc.stat()

    def do_mdi(self, arg, opts=None):
        """execute MDI command"""
        mdi = ''.join(arg)
        self.c.mode(linuxcnc.MODE_MDI)
        self.c.mdi(mdi)

    def do_pos(self, arg, opts=None):
        self.s.poll()
        print self.s.position

mk = MachinekitApp()
mk.cmdloop()

# mah@nwheezy:~/machinekit-polish/src/emc/usr_intf/axis/extensions$ python mksh.py 
# (Cmd) mdi g0 x5
# (Cmd) pos
# (5.0, 2.8450210417129896e-09, 2.91937382162515e-08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
# (Cmd) mdi g0 x0
# (Cmd) pos
# (0.0, 2.8450210417129896e-09, 2.91937382162515e-08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
# (Cmd) mah@nwheezy:~/machinekit-polish/src/emc/usr_intf/axis/extensions$ python mksh.py 
# (Cmd) mdi g0 x0y0z0
# (Cmd) pos
# (0.0, 2.8450210417129896e-09, 2.91937382162515e-08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
# (Cmd) mdi g0 x10 y20
# (Cmd) pos
# (10.0, 20.0, 2.91937382162515e-08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
# (Cmd) 