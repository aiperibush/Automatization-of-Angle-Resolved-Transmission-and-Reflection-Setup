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
from System import String

def main():
    """The main entry point for the application"""

    # Uncomment this line if you are using
    # SimulationManager.Instance.InitializeSimulations()

    try:

        DeviceManagerCLI.BuildDeviceList()

        # create new device
        serial_no = "70280774"  # Replace this line with your device's serial number

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
        # device_info = channel1.GetDeviceInfo()
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

        # Get parameters related to homing/zeroing/other
        homing_params = channel1.GetHomingParams()
        homing_params.Velocity = Decimal(5)
        homing_params.OffsetDistance = Decimal(9)  # real world units
        homing_params.set_Direction(homing_params.Direction.Clockwise)

        channel1.SetHomingParams(homing_params)
        
        # Home or Zero the device (if a motor/piezo)
        # print("Homing Motor")
        # print("homing_params", homing_params)
        # print(dir(homing_params))
        
        channel1.Home(100000)
        print("Done")
        time.sleep(1)
        # print(homing_params.Direction.CounterClockwise.CompareTo(homing_params.Direction.Clockwise))
        # print(dir(homing_params.Direction))

        # Move the device to a new position
        # channel2.SetMoveRelativeDistance(Decimal(0.18335*30)) 
        # channel2.MoveRelative(7000) 
        # time.sleep(3)

        # Stop Polling and Disconnect
        channel1.StopPolling()
        channel2.StopPolling()
        device.Disconnect()

    except Exception as e:
        # this can be bad practice: It sometimes obscures the error source
        print(e)

    # Uncomment this line if you are using Simulations
    # SimulationManager.Instance.UninitializeSimulations()
    ...


if __name__ == "__main__":
    main()
