"""
pythonnet_template
==================

An example written to show control of a BSC101 stepper motor controller.
"""
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

def configure(serial_no):
    
    DeviceManagerCLI.BuildDeviceList()

        # create new device
        # serial_no = "70280774"  # Replace this line with your device's serial number

        # Connect, begin polling, and enable
    device = BenchtopStepperMotor.CreateBenchtopStepperMotor(serial_no)
    device.Connect(serial_no)
    time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device
    
    # For benchtop devices, get the channel   
    channel1 = device.GetChannel(1)
    channel2 = device.GetChannel(2)

    # Ensure that the device settings have been initialized
    if not channel1.IsSettingsInitialized():
        channel1.WaitForSettingsInitialized(10000)  # 10 second timeout
        assert channel1.IsSettingsInitialized() is True
            
    if not channel2.IsSettingsInitialized():
        channel2.WaitForSettingsInitialized(10000)  # 10 second timeout
        assert channel2.IsSettingsInitialized() is True

    # Start polling and enable
    channel1.StartPolling(250)  #250ms polling rate
    channel2.StartPolling(250)
    time.sleep(10)
    channel1.EnableDevice()
    channel2.EnableDevice()
    time.sleep(0.25)  # Wait for device to enable

    # Get Device Information and display description
    device_info = channel1.GetDeviceInfo()
    # print(device_info.Description)

    # Load any configuration settings needed by the controller/stage
    channel_config = channel1.LoadMotorConfiguration(channel1.DeviceID) # If using BSC203, change serial_no to channel.DeviceID. 
    chan_settings = channel1.MotorDeviceSettings

    channel1.GetSettings(chan_settings)

    channel_config.DeviceSettingsName = 'HS NRT150 Enc Stage 150mm'

    channel_config.UpdateCurrentConfiguration()

    channel1.SetSettings(chan_settings, True, False)
        
    channel_config = channel2.LoadMotorConfiguration(channel2.DeviceID) # If using BSC203, change serial_no to channel.DeviceID. 
    chan_settings = channel2.MotorDeviceSettings

    channel2.GetSettings(chan_settings)

    channel_config.DeviceSettingsName = 'HS NRT150 Enc Stage 150mm'

    channel_config.UpdateCurrentConfiguration()

    channel2.SetSettings(chan_settings, True, False)
    
    return channel1, channel2, device

def homing_params (channel1, channel2, velocity):
    # Get parameters related to homing/zeroing/other
    homing_params = channel1.GetHomingParams()
    homing_params.Velocity = Decimal(velocity)
    homing_params.OffsetDistance = Decimal(9)  # real world units
    homing_params.set_Direction(homing_params.Direction.CounterClockwise)
    # homing_params.set_Direction(homing_params.Direction.Clockwise)
        
    homing_params2 = channel2.GetHomingParams()
    homing_params2.Velocity = Decimal(velocity)
    homing_params2.OffsetDistance = Decimal(10)  # real world units
    homing_params2.set_Direction(homing_params2.Direction.CounterClockwise)
    # homing_params2.set_Direction(homing_params2.Direction.Clockwise)

    channel1.SetHomingParams(homing_params)
    channel2.SetHomingParams(homing_params2)
        
    # Home or Zero the device (if a motor/piezo)
    # print("Homing Motor")
    print("homing_params", homing_params.Direction)
    # print(dir(homing_params))

def home1(channel1):        
    channel1.Home(100000)
    print("Done")
    time.sleep(1)

def home2(channel2):
    channel2.Home(100000)
    print("Done")
    time.sleep(1)
    # print(homing_params.Direction.CounterClockwise.CompareTo(homing_params.Direction.Clockwise))
    # print(dir(homing_params.Direction))

def move1(channel1, times, angle):
    # Move the device to a new position
    channel1.MoveTo(Decimal(angle*0.18335), times)
    time.sleep(0.7)

def move2(channel2, times, angle):
    # Move the device to a new position
    channel2.MoveTo(Decimal(angle*0.18335), times) 
    time.sleep(1)

def disconnect(channel1, channel2, device):
    # Stop Polling and Disconnect
    channel1.StopPolling()
    channel2.StopPolling()
    device.Disconnect()

    # Uncomment this line if you are using Simulations
    # SimulationManager.Instance.UninitializeSimulations()
    ...

# channel1, channel2, device = configure('70280774')
# homing_params (channel1, channel2, 5)

#print(f'Homing velocity: {homing_params.Velocity}\n'
#      f'Homing direction: {homing_params.Direction}\n')
# print(dir(channel1.SetMovementSettings))
# jog_params=channel1.GetJogParams()

# jog_params=channel1.GetJogParams()
# jog_params.SetJogStepSize(Decimal(30*0.18335))
# jog_params.SetJogVelocityParams(Decimal(10), Decimal(5)) 
# channel1.SetJogParams(jog_params)



#channel1, channel2, device = configure('70280774')
#homing_params (channel1, channel2, 5)
# home1(channel1)

#channel1.SetJogStepSize(Decimal(30*0.18335))
#channel1.SetJogVelocityParams(Decimal(10), Decimal(5)) 

#new_direction_backward = MotorDirection.Backward

# channel1.MoveJog('Backward', 10000)
#channel1.MoveJog(new_direction_backward, 100000)
#home1(channel1)

print("done")