## Idiot's guide to running Machinekit GUI

* Axis display is known to be a resource hog, especially on little computers like the Pi

* I'm using 'keystick' by setting "display=keystick" instead of "display=axis" in the sim.ini file

* To start machinekit with the config you type 'machinekit keystick.ini' from the directory where the ini file is located

* Exit keystick with ctrl-c

* In Gnome terminal in order to access the F1 key you need to disable keyboard shortcuts (Edit->Preferences->Shortcuts and uncheck the enable shortcuts box)

* Before you can do anything with the gui you need to

1 Disable ESTOP by pushing F1 key (this clears ESTOP and shows 'ESTOP RESET')

2 Turn on the machine with F2 key (this clears ESTOP RESET and shows ON)

3 Press 'Z' key then 'Home' key (for some reason you have to home Z first)

4 Press 'X' key then 'Home' key

5 Press 'Y' key then 'Home' key

Note: You can jog the axes with arrow keys, and pageup/pagedown jog the Z axis

* Once you have the thing homed, press F5 to enter MDI mode

* Then try typing in some G codes for example:

* Fast:

G0 X1 Y1 Z2  

* Slow

G1 X2 F1

* In another command terminal execute halcmd -f -k
* use stuff from [link](http://www.machinekit.io/docs/man/man1/halcmd/)


