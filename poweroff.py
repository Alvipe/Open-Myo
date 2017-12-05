import open_myo as myo

myo_mac_addr = myo.get_myo()
myo_device = myo.Device()
myo_device.services.power_off()
