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

def measure(start, end, step, integration): #no negative degree inputs, instead of -90 use 270. also don't mix up start and end
    home1(channel1)
    # print("start movement")
    move(channel1, 60000, start)
    measurements={"Angles":[], "Wavelength":[], "Intensity":[]}
    spec=Connect()
    measurements["Wavelength"].append(['{:.2f}'.format(i) for i in spec.wavelengths()])

    plt.ion()
    grid_kws = {'width_ratios': (0.9, 0.05), 'wspace': 0.2}
    fig, (ax, cbar_ax) = plt.subplots(1, 2, gridspec_kw = grid_kws, figsize = (10, 8))
    ax.xaxis.set_tick_params(which='both', direction='out', length=1)
    ax.yaxis.set_tick_params(which='both', direction='out', length=1)
    ax.locator_params(axis='x', nbins=6)
    ax.locator_params(axis='y', nbins=10)
    for i in range(math.floor(((360-start)+end+1)/step)): 
        move(channel1, 6000, start+(i*step))
        measurements["Angles"].append((-(360-start))+step*i) 
        measurements["Intensity"].append(spectrometer(spec, integration))
        df=pd.DataFrame(measurements["Intensity"], index=tuple(measurements["Angles"]), columns=measurements["Wavelength"])
        ax=sns.heatmap(df, ax=ax, cbar_ax = cbar_ax, cmap="mako", linewidths=0)
        # fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.5)
    plt.show()
    df.to_csv("samplex1y1.csv", index=True)
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
# grid=np.meshgrid(measurements["Wavelength"] ,measurements["Angles"])

   
channel1.StopPolling()
channel2.StopPolling()
device.Disconnect()