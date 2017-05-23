import sys
import struct
import time
from bluepy import btle

class Services(btle.Peripheral):
    # Bluepy's Peripheral class encapsulates a connection to a Bluetooth LE peripheral
    def __init__(self, mac):
        btle.Peripheral.__init__(self, mac)
        time.sleep(0.5)

    def firmware(self):
        hex_fw = self.readCharacteristic(0x17)
        fw = struct.unpack('<4h', hex_fw)
        return fw

    def battery(self):
        hex_batt = self.readCharacteristic(0x11)
        batt = ord(hex_batt)
        return batt

    def set_leds(self, logo, line):
        self.writeCharacteristic(0x19, struct.pack('8B', 6, 6, *(logo + line)))

    def battery_notifications(self):
        self.writeCharacteristic(0x12, b'\x01\x10')

    def emg_notifications(self):
        self.writeCharacteristic(0x2c, b'\x01\x00')
        self.writeCharacteristic(0x2f, b'\x01\x00')
        self.writeCharacteristic(0x32, b'\x01\x00')
        self.writeCharacteristic(0x35, b'\x01\x00')

    def imu_notifications(self):
        self.writeCharacteristic(0x1d, b'\x01\x00')

    def classifier_notifications(self):
        self.writeCharacteristic(0x24, b'\x02\x00')


class Device(btle.DefaultDelegate):
    # bluepy functions which receive Bluetooth messages asynchronously,
    # such as notifications, indications, and advertising data
    def __init__(self, mac=None):
        btle.DefaultDelegate.__init__(self)
        self.services = Services(mac=get_myo(mac))
        self.services.setDelegate(self)

def get_myo(mac=None):
    if mac is not None:
        while True:
            for i in btle.Scanner(0).scan(1):
                if i.addr == mac:
                    return str(mac).upper()

    while True:
        for i in btle.Scanner(0).scan(1):
            for j in i.getScanData():
                if j[0] == 6 and j[2] == '4248124a7f2c4847b9de04a9010006d5':
                    return str(i.addr).upper()

# From here on, all shit

# EMG_HANDLE = 0x27
#
# def multichr(ords):
#     if sys.version_info[0] >= 3:
#         return bytes(ords)
#     else:
#         return ''.join(map(chr, ords))
#
# def multiord(b):
#     if sys.version_info[0] >= 3:
#         return list(b)
#     else:
#         return map(ord, b)
#
# def getMyo(mac=None):
#     if mac is not None:
#         while True:
#             for i in btle.Scanner(0).scan(1):
#                 if i.addr == mac:
#                     return str(mac).upper()
#
#     while True:
#         for i in btle.Scanner(0).scan(1):
#             for j in i.getScanData():
#                 if j[0] == 6 and j[2] == '4248124a7f2c4847b9de04a9010006d5':
#                     return str(i.addr).upper()
#
# def connectMyo(mac=None):
#     myo = btle.Peripheral(mac)
#     return myo
#
# def firmware(myo):
#     fw = myo.readCharacteristic(0x17)
#     fw = struct.unpack('<4h', fw)
#     return fw
#
# def suscribeEmg(myo):
#     myo.writeCharacteristic(0x2c, b'\x01\x00')
#     myo.writeCharacteristic(0x2f, b'\x01\x00')
#     myo.writeCharacteristic(0x32, b'\x01\x00')
#     myo.writeCharacteristic(0x35, b'\x01\x00')
#     myo.writeCharacteristic(0x19, b'\x01\x03\x02\x00\x00')
#
# class MyoDevice(btle.DefaultDelegate):
#     def __init__(self, mac=None):
#         btle.DefaultDelegate.__init__(self)
#         self.myo = connectMyo(mac = getMyo(mac))
#         self.myo.setDelegate(self)
#
#     def handleNotification(self, cHandle, data):
#         if cHandle == 0x2b or cHandle == 0x2e or cHandle == 0x31 or cHandle == 0x34:
#             # '''According to http://developerblog.myo.com/myocraft-emg-in-the-bluetooth-protocol/
#             # each characteristic sends two secuential readings in each update,
#             # so the received payload is split in two samples. According to the
#             # Myo BLE specification, the data type of the EMG samples is int8_t.
#             # '''
#             # emg1 = struct.unpack('<8b', pay[:8])
#             # emg2 = struct.unpack('<8b', pay[8:])
#             # self.on_emg(emg1, 0)
#             # self.on_emg(emg2, 0)
#             emg1 = struct.unpack('<8b', data[:8])
#             emg2 = struct.unpack('<8b', data[8:])
#             print(emg1)
#             print(emg2)
#
# class MyoFunctions(object):
#     pass
