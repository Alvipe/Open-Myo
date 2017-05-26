import open_myo as myo

myo_mac_addr = myo.get_myo()
print("MAC address: %s" % myo_mac_addr)
myo_device = myo.Device()
myo_device.services.set_leds([128, 128, 255], [128, 128, 255])  # purple logo and bar LEDs)
myo_device.services.vibrate(1) # short vibration
fw = myo_device.services.firmware()
print("Firmware version: %d.%d.%d.%d" % (fw[0], fw[1], fw[2], fw[3]))
batt = myo_device.services.battery()
print("Battery level: %d" % batt)
myo_device.services.emg_filt_notifications()
# myo_device.services.emg_raw_notifications()
myo_device.services.imu_notifications()
# myo_device.services.battery_notifications()
myo_device.services.set_mode(myo.emg_mode.FILT, myo.imu_mode.ALL, myo.classifier_mode.OFF)
while True:
    if myo_device.services.waitForNotifications(1):
        continue
    print("Waiting...")
