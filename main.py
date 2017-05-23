import open_myo as myo

myo_mac_addr = myo.get_myo()
print(myo_mac_addr)
myo_device = myo.Device()
myo_device.services.set_leds([128, 128, 255], [128, 128, 255])  # purple logo and bar LEDs)
print(myo_device.services.battery())

# myOjete = myo.MyoDevice()
# myo.suscribeEmg(myOjete.myo)
# while True:
#     myOjete.myo.waitForNotifications(1)

# myOjete = myo.connectMyo(myo.getMyo())
# fw = myo.firmware(myOjete)
# print('firmware version: %d.%d.%d.%d' % (fw[0], fw[1], fw[2], fw[3]))
