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
import numpy as np
from matplotlib.ticker import FuncFormatter

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
    # print("start movement")
    move(channel1, 60000, start)
    measurements={"Angles":[], "Wavelength":[], "Intensity":[]}
    spec=Connect()
    measurements["Wavelength"].append(['{:.2f}'.format(i) for i in spec.wavelengths()])

    for i in range(math.floor(((360-start)+end)/step)): 
        move(channel1, 6000, start+(i*step))
        measurements["Angles"].append((start+i)%360) 
        measurements["Intensity"].append(spectrometer(spec, integration))
        time.sleep(0.5)
    return measurements


def saveCSV(measurements, name):
    df=pd.DataFrame(measurements)
    df.to_csv(name)
    
def saveExcel(measurements, name):
    df=pd.DataFrame(measurements)
    df.to_excel(name)

measurements=measure(300, 60, 1, 100000)

df=pd.DataFrame(measurements["Intensity"], index=tuple(measurements["Angles"]), columns=measurements["Wavelength"])
pd.options.display.float_format="{:.2f}".format
# df.update(df.columns.applymap('{:.2f}'.format))
print(df)
df.to_csv("test.csv", index=True)
# grid=np.meshgrid(measurements["Wavelength"] ,measurements["Angles"])

# fig = plt.figure(1, figsize=(6, 9))
# ax = fig.add_subplot(111)
# print(np.shape(measurements["Intensity"]))
               
        #plt.pcolormesh(radii, lambdas, (tab1).transpose(), cmap = 'rainbow') #plt.cm.RdBu)
# heatmap = ax.pcolormesh(measurements["Angles"], measurements["Wavelength"], 0, cmap = plt.cm.viridis, alpha=1) #plt.cm.RdBu)
        #plt.title("Absorptance, Unit", pad = 50, fontsize=12)
plt.figure(figsize=(5,5))
ax=sns.heatmap(df, cmap="mako", linewidths=0)
# ax.xaxis.set_major_formatter(FuncFormatter('{:.2f}'.format))
plt.show()
# saveExcel(measurements, "testSpec.xlsx")
   
channel1.StopPolling()
channel2.StopPolling()
device.Disconnect()