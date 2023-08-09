from kinesis import *
from powerMeter import *

import os
import time
import sys
import clr #if this won't import than check pythonnet documentation for install and config guide
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")  #be sure kinesis is downloaded otherwise these lines will give errors
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import * 
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import *
from System import Decimal  # necessary for real world units

channel1, channel2, device = configure('70280774') #serial number of benchtop, if you replace the benchtop you'll need to change this
homing_params (channel1, channel2, 5) #homing function, refer to kinesis.py if you need to change any homing parameters
# channel1.DeviceSettingsName = 'HDR50' 
tlpm=connect() #power meter function, refer to powerMeter.py
wavelength(tlpm, 532) #always remember to set the wavelength here every time you run the code
home1(channel1) #homing, this needs to be done before you run the code every time, otherwise the motor will not move

# print("start movement")
move(channel1, 60000, 300) #60000 milliseconds until timeout, move 300 degrees
measurements={"Angles":[], "Power":[]}

sns.set_theme(context="paper", style="ticks")
# ax=sns.scatterplot(data=measurements, x="Angles", y="Power", color="chartreuse")

plt.ion() #creates real time plot that refreshes constantly
for i in range(121):
    move(channel1, 6000, 300+i)
    measurements["Angles"].append(-60+i)
    measurements["Power"].append(measure(tlpm))
    plt.plot(measurements["Angles"], measurements["Power"], c='indigo') #these lines can be removed if you don't want real time plot
    plt.title("Real Time plot")
    plt.xlabel("Angle (degrees)")
    plt.ylabel("Power")
    plt.pause(0.05)
    
plt.show()
plt.savefig("graph.png")

print(measurements)

def saveCSV(measurements, name):
    df=pd.DataFrame(measurements)
    df.to_csv(name)
    
def saveExcel(measurements, name):
    df=pd.DataFrame(measurements)
    df.to_excel(name)
    
saveCSV(measurements, "thing.csv")
    
channel1.StopPolling()
channel2.StopPolling()
device.Disconnect()
tlpm.close()