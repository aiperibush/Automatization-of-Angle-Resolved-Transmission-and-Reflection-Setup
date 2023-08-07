from kinesis import *
from spectrometer import *

import os
import time
import sys
import clr
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import *
from System import Decimal  # necessary for real world units

channel1, channel2, device = configure('70280774')
homing_params (channel1, channel2, 5)

def measure(start, end, step, integration):
    home1(channel1)
    print("start movement")
    move(channel1, 60000, start)
    measurements={"Angles":[], "Wavelength":[], "Intensity":[]}
    spec=Connect()
    measurements["Wavelength"]=spec.wavelengths()

    for i in range(math.floor(abs(end-start)/step)):
        move(channel1, 6000, start+(i*step))
        measurements["Angles"].append(-start+i)
        measurements["Intensity"].append(list(spectrometer(spec, integration)))
        time.sleep(0.5)
    return measurements


def saveCSV(measurements, name):
    df=pd.DataFrame(measurements)
    df.to_csv(name)
    
def saveExcel(measurements, name):
    df=pd.DataFrame(measurements)
    df.to_excel(name)

measurements=measure(300, 60, 1, 100000)
print(len(measurements["Intensity"]))
saveCSV(measurements, "testSpec.csv")
    
channel1.StopPolling()
channel2.StopPolling()
device.Disconnect()