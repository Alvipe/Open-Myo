# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 10:33:36 2015

@author: Alvaro
"""

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline

def segmentation(emg, samples = 150):
    N = samples # number of samples per segment
    S = int(np.floor(emg.shape[0]/N)) # number of segments
    length = 0
    segmented_emg = np.zeros((N,S))
    for s in range(S):
        for n in range(length,N+length):
            segmented_emg[n-length,s] = emg[n] # 2D matrix with a EMG signal divided in s segments, each one with n samples
        length = length + N
    length = 0
    return segmented_emg

def mav(segment):
    mav = np.mean(np.abs(segment))
    return mav

def rms(segment):
    rms = np.sqrt(np.mean(np.power(segment,2)))
    return rms

def var(segment):
    var = np.var(segment)
    return var

def ssi(segment):
    ssi = np.sum(np.abs(np.power(segment,2)))
    return ssi

def zc(segment):
    nz_segment = []
    nz_indices = np.nonzero(segment)[0] #Finds the indices of the segment with nonzero values
    for m in nz_indices:
        nz_segment.append(segment[m]) #The new segment contains only nonzero values    
    N = len(nz_segment)
    zc = 0
    for n in range(N-1):
        if((nz_segment[n]*nz_segment[n+1]<0) and np.abs(nz_segment[n]-nz_segment[n+1]) >= 1e-4):
            zc = zc + 1
    return zc

def wl(segment):
    wl = np.sum(np.abs(np.diff(segment)))
    return wl

#def ssc(segment):
#    N = len(segment)
#    ssc = 0
#    for n in range(1,N-1):
#        if (segment[n]-segment[n-1])*(segment[n]-segment[n+1])>=1e-4:
#            ssc += 1
#    return ssc

def ssc(segment):
    N = len(segment)
    ssc = 0
    for n in range(1,N-1):
        if ((segment[n]>segment[n-1] and segment[n]>segment[n+1]) or (segment[n]<segment[n-1] and segment[n]<segment[n+1]) and ((np.abs(segment[n]-segment[n+1])>=1e-4) or (np.abs(segment[n]-segment[n-1])>=1e-4))):
            ssc += 1
    return ssc

def wamp(segment):
    N = len(segment)
    wamp = 0
    for n in range(N-1):
        if np.abs(segment[n]-segment[n+1])>1e-4:
            wamp += 1
    return wamp

def features(segment,feature_list):
    features = np.zeros((1,len(segment)*len(feature_list)))
    i = 0
    for feature in feature_list:
        features[0,i] = feature(segment[0])
        features[0,i+1] = feature(segment[1])
        features[0,i+2] = feature(segment[2])
        features[0,i+3] = feature(segment[3])
        features[0,i+4] = feature(segment[4])
        features[0,i+5] = feature(segment[5])
        features[0,i+6] = feature(segment[6])        
        features[0,i+7] = feature(segment[7])
        i +=  len(segment)
    return features

def feature_scaling(feature_matrix,target,reductor=None,scaler=None):
    lda = LDA(n_components=2)    
    minmax = MinMaxScaler(feature_range=(-1,1))
    if not reductor:
        reductor = lda.fit(feature_matrix,target)
    feature_matrix_lda = reductor.transform(feature_matrix)
    if not scaler:
        scaler = minmax.fit(feature_matrix_lda)
    feature_matrix_scaled = scaler.transform(feature_matrix_lda)
    return feature_matrix_scaled,reductor,scaler

def gestures(nSamples,nGestures):
    gestures = []
    for m in range(nGestures):
        gestures.append((m*np.ones((nSamples))))
    gestures = np.array(gestures).ravel()
    return gestures

#def feature_scaling(feature_matrix,target,scaler=None):
#    lda = LDA(n_components=2)    
#    minmax = MinMaxScaler(feature_range=(-1,1))
#    if not scaler:
#        scaler = make_pipeline(lda,minmax)
#        scaler.fit(feature_matrix,target)
#    feat_lda_scaled = scaler.transform(feature_matrix)
#    
#    return feat_lda_scaled,scaler