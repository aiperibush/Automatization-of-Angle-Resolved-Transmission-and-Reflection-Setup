from seabreeze.spectrometers import Spectrometer, list_devices

def Connect():
    devices = list_devices()
    spec = Spectrometer(devices[0])
    print("connected")
    return spec

def spectrometer(spec, integration):
    spec.integration_time_micros(integration)
    intensities = spec.intensities()
    return intensities