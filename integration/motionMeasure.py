from kinesis import *
from powerMeter import *

channel1, channel2, device = configure('70280774')
homing_params (channel1, channel2, 5)
# tlpm=connect()
# wavelength(tlpm, 650)
move1(channel1, 7000, 30)
move1(channel1, 7000, -30)
# tlpm.close()