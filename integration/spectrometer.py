from seabreeze.spectrometers import Spectrometer, list_devices
devices = list_devices()
print(devices)
spec = Spectrometer(devices[0])
spec.integration_time_micros(100000)
wavelengths = spec.wavelengths()
print("Wavelengths:", wavelengths)
intensities = spec.intensities()
print("Intensities:", intensities)