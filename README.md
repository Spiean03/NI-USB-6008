# NI-USB6008-analog-digital-outputs

This script allows to control analog (any value between 0 and 5V) and digital (0 or 5V) outputs of the USB-6008 DAQ from National Instrument using the PyDAQmx module. 
Additional outputs can be added following the same model.



1) Import the code
2) Instantiate the class. Here you the sting you specify sets what DAQ you want to access (in this case the it's Dev1) and what ports you would like to monitor (in this case analogue input ports 0 through to 2).
3) Returns a Python (indexed by port number) of voltages
3) Returns a Python of currents

import DAQ
daq = DAQ("Dev1/ai0:2")
volts = daq.voltage()
amps  = daq.current()
