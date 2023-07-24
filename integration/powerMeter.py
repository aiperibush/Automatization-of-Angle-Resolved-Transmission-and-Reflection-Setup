from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
from TLPM import TLPM
import time

def connect():
    tlPM = TLPM()
    deviceCount = c_uint32()
    # Find connected power meter devices.
    tlPM.findRsrc(byref(deviceCount))
    resourceName = create_string_buffer(1024)

    for i in range(0, deviceCount.value):
        tlPM.getRsrcName(c_int(i), resourceName)
        # print("Resource name of device", i, ":", c_char_p(resourceName.raw).value)
    # print("")
    tlPM.close()
    # Connect to last device.
    tlPM = TLPM()
    tlPM.open(resourceName, c_bool(True), c_bool(True))

    message = create_string_buffer(1024)
    tlPM.getCalibrationMsg(message)
    print("Connected to device", i)
    print("Last calibration date: ",c_char_p(message.raw).value)
    print("")
    return tlPM
    time.sleep(2)





# print("Number of found devices: " + str(deviceCount.value))
# print("")





def wavelength(tlPM, wavelength): # Set wavelength in nm.
    tlPM.setWavelength(c_double(wavelength))
    tlPM.setPowerAutoRange(c_int16(1))
    tlPM.setPowerUnit(c_int16(0))


# Enable auto-range mode.
# 0 -> auto-range disabled
# 1 -> auto-range enabled


# Set power unit to Watt.
# 0 -> Watt
# 1 -> dBm


# Take power measurements and save results to arrays.
# power_measurements = []
# times = []
def measure(tlPM):
    power =  c_double()
    tlPM.measPower(byref(power))
    measurement=power.value
    return measurement

# measurements=[]
#     count = time.time()
#     while time.time()-count<3600:
#         power =  c_double()
#         tlPM.measPower(byref(power))
#         measurements.append(list((time.time()-count, power.value)))
#     # power_measurements.append(power.value)
#     # times.append(datetime.now())
#     # print(time.time()-count, ":", power_measurements[count], "W")
    
#         time.sleep(1)

# Close power meter connection.
def disconnect(tlPM):
    tlPM.close()
print('End program')