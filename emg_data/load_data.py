# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:59:59 2018

@author: alvaro
"""

import pickle
import matplotlib.pyplot as plt

filename = "emg_data_20180206-165445.pkl"

channel_0 = list()
channel_1 = list()
channel_2 = list()
channel_3 = list()
channel_4 = list()
channel_5 = list()
channel_6 = list()
channel_7 = list()

with open(filename, 'r') as fp:
    emg_data = pickle.load(fp)

for i in range(len(emg_data)):
    channel_0.append(emg_data[i][0])
    channel_1.append(emg_data[i][1])
    channel_2.append(emg_data[i][2])
    channel_3.append(emg_data[i][3])
    channel_4.append(emg_data[i][4])
    channel_5.append(emg_data[i][5])
    channel_6.append(emg_data[i][6])
    channel_7.append(emg_data[i][7])

plt.figure()
plt.plot(channel_0)
plt.show()