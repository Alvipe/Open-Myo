import sys
import struct
import time
from enum import Enum
from bluepy import btle

class Services(btle.Peripheral):
    # Bluepy's Peripheral class encapsulates a connection to a Bluetooth LE peripheral
    def __init__(self, mac):
        btle.Peripheral.__init__(self, mac)
        time.sleep(0.5)

    # Get the firmware version
    def firmware(self):
        hex_fw = self.readCharacteristic(ReadHandle.FIRMWARE)
        fw = struct.unpack('<4h', hex_fw)
        return fw

    # Get the battery level
    def battery(self):
        hex_batt = self.readCharacteristic(ReadHandle.BATTERY)
        batt = ord(hex_batt)
        return batt

    # Change the color of the logo and bar LEDs
    def set_leds(self, logo, line):
        self.writeCharacteristic(WriteHandle.COMMAND, struct.pack('<8B', 6, 6, *(logo + line)))

    def vibrate(self, length):
        if length in range(1, 4):
            self.writeCharacteristic(WriteHandle.COMMAND, struct.pack('<3B', 3, 1, length))

    def sleep_mode(self, mode):
        self.writeCharacteristic(WriteHandle.COMMAND, struct.pack('<3B', 9, 1, mode))

    def power_off(self):
        self.writeCharacteristic(WriteHandle.COMMAND, b'\x04\x00')

    # Suscribe to battery notifications
    def battery_notifications(self):
        self.writeCharacteristic(WriteHandle.BATTERY, b'\x01\x10')

    # Suscribe to raw EMG notifications
    def emg_raw_notifications(self):
        self.writeCharacteristic(WriteHandle.EMG0, b'\x01\x00')
        self.writeCharacteristic(WriteHandle.EMG1, b'\x01\x00')
        self.writeCharacteristic(WriteHandle.EMG2, b'\x01\x00')
        self.writeCharacteristic(WriteHandle.EMG3, b'\x01\x00')

    # Suscribe to filtered EMG notifications
    def emg_filt_notifications(self):
        self.writeCharacteristic(WriteHandle.EMG_FILT, b'\x01\x00')

    # Suscribe to IMU notifications
    def imu_notifications(self):
        self.writeCharacteristic(WriteHandle.IMU, b'\x01\x00')

    # Suscribe to classifier notifications
    def classifier_notifications(self):
        self.writeCharacteristic(WriteHandle.CLASSIFIER, b'\x02\x00')

    def set_mode(self, emg_mode, imu_mode, classifier_mode):
        command_string = struct.pack('<5B', 1, 3, emg_mode, imu_mode, classifier_mode)
        self.writeCharacteristic(WriteHandle.COMMAND, command_string)

class Device(btle.DefaultDelegate):
    # bluepy functions which receive Bluetooth messages asynchronously,
    # such as notifications, indications, and advertising data
    def __init__(self, mac=None):
        btle.DefaultDelegate.__init__(self)
        self.services = Services(mac=get_myo(mac))
        self.services.setDelegate(self)

        self.emg_event_handlers = []
        self.imu_event_handlers = []
        self.sync_event_handlers = []
        self.classifier_event_handlers = []
        self.battery_event_handlers = []

    def handleNotification(self, cHandle, data):
        # Notification handles of the 4 EMG data characteristics (raw)
        if cHandle == ReadHandle.EMG0 or cHandle == ReadHandle.EMG1 or cHandle == ReadHandle.EMG2 or cHandle == ReadHandle.EMG3:
            '''According to http://developerblog.myo.com/myocraft-emg-in-the-bluetooth-protocol/
            each characteristic sends two secuential readings in each update,
            so the received payload is split in two samples. According to the
            Myo BLE specification, the data type of the EMG samples is int8_t.
            '''
            emg_raw = []
            emg1 = struct.unpack('<8b', data[:8])
            emg2 = struct.unpack('<8b', data[8:])
            emg_raw.append(emg1)
            emg_raw.append(emg2)
            self.on_emg(emg_raw)
        # Notification handle of the EMG data characteristic (filtered)
        elif cHandle == ReadHandle.EMG_FILT:
            emg_filt = struct.unpack('<8H', data[:16])
            self.on_emg(emg_filt)
        # Notification handle of the IMU data characteristic
        elif cHandle == ReadHandle.IMU:
            values = struct.unpack('<10h', data)
            quat = [x/16384.0 for x in values[:4]]
            acc = [x/2048.0 for x in values[4:7]]
            gyro = [x/16.0 for x in values[7:10]]
            self.on_imu(quat, acc, gyro)
        # Notification handle of the classifier data characteristic
        elif cHandle == ReadHandle.CLASSIFIER:
            event_type, value, x_direction, _, _, _ = struct.unpack('<6B', data)
            if event_type == ClassifierEventType.ARM_SYNCED:  # on arm
                self.on_sync(Arm(value), XDirection(x_direction))
            elif event_type == ClassifierEventType.ARM_UNSYNCED:  # removed from arm
                self.on_sync(Arm.UNKNOWN, XDirection.UNKNOWN)
            elif event_type == ClassifierEventType.POSE:  # pose
                self.on_classifier(Pose(value))
            elif event_type == ClassifierEventType.SYNC_FAILED:
                print("Sync failed, please perform sync gesture.")
        # Notification handle of the battery data characteristic
        elif cHandle == ReadHandle.BATTERY:
            batt = ord(data)
            self.on_battery(batt)
        else:
            print('Data with unknown attr: %02X' % cHandle)

    def add_emg_event_handler(self, event_handler):
        self.emg_event_handlers.append(event_handler)

    def add_imu_event_handler(self, event_handler):
        self.imu_event_handlers.append(event_handler)

    def add_sync_event_handler(self, event_handler):
        self.sync_event_handlers.append(event_handler)

    def add_classifier_event_hanlder(self, event_handler):
        self.classifier_event_handlers.append(event_handler)

    def add_battery_event_handler(self, event_handler):
        self.battery_event_handlers.append(event_handler)

    def on_emg(self, emg):
        for event_handler in self.emg_event_handlers:
            event_handler(emg)

    def on_imu(self, quat, acc, gyro):
        for event_handler in self.imu_event_handlers:
            event_handler(quat, acc, gyro)

    def on_sync(self, arm, x_direction):
        for event_handler in self.sync_event_handlers:
            event_handler(arm, x_direction)

    def on_classifier(self, pose):
        for event_handler in self.classifier_event_handlers:
            event_handler(pose)

    def on_battery(self, batt):
        for event_handler in self.battery_event_handlers:
            event_handler(batt)

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

class ReadHandle:
    BATTERY = 0x11
    FIRMWARE = 0x17
    EMG0 = 0x2b
    EMG1 = 0x2e
    EMG2 = 0x31
    EMG3 = 0x34
    EMG_FILT = 0x27
    IMU = 0x1c
    CLASSIFIER = 0x23

class WriteHandle:
    COMMAND = 0x19
    BATTERY = 0x12
    EMG0 = 0x2c
    EMG1 = 0x2f
    EMG2 = 0x32
    EMG3 = 0x35
    EMG_FILT = 0x28
    IMU = 0x1d
    CLASSIFIER = 0x24

class EmgMode:
    OFF = 0x00
    FILT = 0x01
    RAW = 0x02
    RAW_UNFILT = 0x03

class ImuMode:
    OFF = 0x00
    DATA = 0x01
    EVENTS = 0x02
    ALL = 0x03
    RAW = 0x04

class ClassifierMode:
    OFF = 0x00
    ON = 0x01

class ClassifierEventType:
    ARM_SYNCED = 0x01
    ARM_UNSYNCED = 0x02
    POSE = 0x03
    UNLOCKED = 0x04
    LOCKED = 0x05
    SYNC_FAILED = 0x06

class Pose(Enum):
    REST = 0x00
    FIST = 0x01
    WAVE_IN = 0x02
    WAVE_OUT = 0x03
    FINGERS_SPREAD = 0x04
    DOUBLE_TAP = 0x05
    UNKNOWN = 0xff

class Arm(Enum):
    RIGHT = 0x01
    LEFT = 0x02
    UNKNOWN = 0xff

class XDirection(Enum):
    WRIST = 0x01
    ELBOW = 0x02
    UNKNOWN = 0xff
