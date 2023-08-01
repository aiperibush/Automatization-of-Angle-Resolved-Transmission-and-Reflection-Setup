from kinesis import *
from powerMeter import *

import os
import time
import sys
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import *
from System import Decimal  # necessary for real world units

channel1, channel2, device = configure('70280774')
homing_params (channel1, channel2, 5)
tlpm=connect()
wavelength(tlpm, 600)
home1(channel1)

print("start movement")
move1(channel1, 60000, 330)
measurements={"Angles":[], "Power":[]}
for i in range(181):
    move1(channel1, 60000, 270+i)
    measurements["Angles"].append([-90+i])
    measurements["Power"].append(measure(tlpm))


print(measurements)
channel1.StopPolling()
channel2.StopPolling()
device.Disconnect()
tlpm.close()