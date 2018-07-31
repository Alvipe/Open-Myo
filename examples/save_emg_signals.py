#  Copyright 2018 Alvaro Villoslada (Alvipe)
#  This file is part of Open Myo.
#  Open Myo is distributed under a GPL 3.0 license

import open_myo as myo
import numpy as np
import timeit
import time
import pickle

get_reading = False

def process_emg(emg):
    if get_reading:
        gestures[name][i].append(emg[0])
        gestures[name][i].append(emg[1])
#        emg_values.append(emg[0])
#        emg_values.append(emg[1])

def save_data(data):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = "emg_data_"+timestr
    with open("emg_data/"+filename+".pkl", 'wb') as fp:
        pickle.dump(data, fp)

myo_device = myo.Device()
myo_device.services.sleep_mode(1) # never sleep
myo_device.services.set_leds([128, 128, 255], [128, 128, 255])  # purple logo and bar LEDs)
myo_device.services.vibrate(1) # short vibration
# myo_device.services.emg_filt_notifications()
myo_device.services.emg_raw_notifications()
myo_device.services.set_mode(myo.EmgMode.RAW, myo.ImuMode.OFF, myo.ClassifierMode.OFF)
#myo_device.services.set_mode(myo.EmgMode.OFF, myo.ImuMode.OFF, myo.ClassifierMode.OFF)
time.sleep(1)
myo_device.add_emg_event_handler(process_emg)

gestures = dict()
n_gestures = int(raw_input("How many gestures do you want to perform?: "))
n_iterations = int(raw_input("How many times do you want to repeat each gesture?: "))
runtime = int(raw_input("How many seconds do you want each gesture to last?: ")) 

for g in range(n_gestures):
    name = raw_input("Enter the name of gesture number {}: ".format(g+1))
    gestures[name] = list()
    for i in range(n_iterations):
        gestures[name].append(list())
        raw_input("Iteration {}. Press enter to begin recording.".format(i+1))
        myo_device.services.vibrate(1) # short vibration
        time.sleep(2)
#        myo_device.services.set_mode(myo.EmgMode.RAW, myo.ImuMode.OFF, myo.ClassifierMode.OFF)
        start_time = timeit.default_timer()
        tick = start_time
        get_reading = True
        while round(tick - start_time, 1) <= runtime:
            if myo_device.services.waitForNotifications(1):
                tick = timeit.default_timer()
#                continue
            else:
                print("Waiting...")
#        myo_device.services.set_mode(myo.EmgMode.OFF, myo.ImuMode.OFF, myo.ClassifierMode.OFF)
        get_reading = False
        myo_device.services.vibrate(1) # short vibration
        time.sleep(2)

save_data(gestures)
print(tick - start_time)   
