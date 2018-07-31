#  Copyright 2018 Alvaro Villoslada (Alvipe)
#  This file is part of Open Myo.
#  Open Myo is distributed under a GPL 3.0 license

import open_myo as myo

myo_mac_addr = myo.get_myo()
myo_device = myo.Device()
myo_device.services.power_off()
