from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
from TLPM import TLPM
import time


# Find connected power meter devices.
tlPM = TLPM()
deviceCount = c_uint32()
tlPM.findRsrc(byref(deviceCount))

print("Number of found devices: " + str(deviceCount.value))
print("")

resourceName = create_string_buffer(1024)

for i in range(0, deviceCount.value):
    tlPM.getRsrcName(c_int(i), resourceName)
    print("Resource name of device", i, ":", c_char_p(resourceName.raw).value)
print("")
tlPM.close()

# Connect to last device.
tlPM = TLPM()
tlPM.open(resourceName, c_bool(True), c_bool(True))

message = create_string_buffer(1024)
tlPM.getCalibrationMsg(message)
print("Connected to device", i)
print("Last calibration date: ",c_char_p(message.raw).value)
print("")

time.sleep(2)

def wavelength(wavelength): # Set wavelength in nm.
    tlPM.setWavelength(c_double(wavelength))
wavelength(400)


# Enable auto-range mode.
# 0 -> auto-range disabled
# 1 -> auto-range enabled
tlPM.setPowerAutoRange(c_int16(1))

# Set power unit to Watt.
# 0 -> Watt
# 1 -> dBm
tlPM.setPowerUnit(c_int16(0))

# Take power measurements and save results to arrays.
# power_measurements = []
# times = []
measurements=[]
count = time.time()
while time.time()-count<3600:
    power =  c_double()
    tlPM.measPower(byref(power))
    measurements.append(list((time.time()-count, power.value)))
    # power_measurements.append(power.value)
    # times.append(datetime.now())
    # print(time.time()-count, ":", power_measurements[count], "W")
    
    time.sleep(1)
print(measurements)

# Close power meter connection.
tlPM.close()
print('End program')