# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 19:12:54 2018

@author: Alvaro
"""

from emgesture import fextraction as fex
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import pickle

# Data loading
with open("../emg_data/emg_data_20180210-145505.pkl",'r') as fp:
    gestures = pickle.load(fp)

nGestures = len(gestures)
nIterations = [len(value) for value in gestures.values()][0]
nChannels = 8
nSignals = nGestures*nIterations*nChannels
emg = list()
segmented_emg = list()

#for m in range(1,nGestures+1):
#    for i in range(nIterations):
#        for c in range(1,nChannels+1):
#            emg.append(emg_data['motion'+str(m)+'_ch'+str(c)][:,i]) #motion1_ch1_i1, motion1_ch2_i1, motion1_ch1_i2, motion1_ch2_i2

for g in gestures.keys():
    for i in range(nIterations):
        for c in range(nChannels):
            emg.append(np.array(zip(*gestures[g][i])[c][0:999]))

#for z in range(nSignals):
#    emg[z] = emg[z]*(5/2)/2**24

# Segmentation
for n in range(nSignals):
    segmented_emg.append(fex.segmentation(emg[n],samples=50))

# Feature calculation
feature_list = [fex.mav, fex.rms, fex.var, fex.ssi, fex.zc, fex.wl, fex.ssc, fex.wamp]

nSegments = len(segmented_emg[0][0])
nFeatures = len(feature_list)
feature_matrix = np.zeros((nGestures*nIterations*nSegments,nFeatures*nChannels))
n = 0

for i in range(0,nSignals,nChannels):
    for j in range(nSegments):
        feature_matrix[n] = fex.features((segmented_emg[i][:,j],
                                          segmented_emg[i+1][:,j],
                                          segmented_emg[i+2][:,j],
                                          segmented_emg[i+3][:,j],
                                          segmented_emg[i+4][:,j],
                                          segmented_emg[i+5][:,j],
                                          segmented_emg[i+6][:,j],
                                          segmented_emg[i+7][:,j]),feature_list)
        n = n + 1

# Target matrix generation
y = fex.gestures(nIterations*nSegments,nGestures)

# Dimensionality reduction and feature scaling
[X,reductor,scaler] = fex.feature_scaling(feature_matrix, y)

# Split dataset into training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Classifier training
classifier = SVC(kernel='rbf',C=10,gamma=10)
classifier.fit(X_train,y_train)

# Classification
predict = classifier.predict(X_test)
print("Classification accuracy = %0.5f." %(classifier.score(X_test,y_test)))

## Cross validation (optional; takes a lot of time)
#from sklearn.cross_validation import StratifiedShuffleSplit
#from sklearn.grid_search import GridSearchCV
#from sklearn.svm import SVC
#
#C_range = np.logspace(-5,5,11)
#gamma_range = np.logspace(-30,1,32)
#param_grid = dict(gamma=gamma_range,C=C_range)
#cv = StratifiedShuffleSplit(y, n_iter=20,test_size=0.2,random_state=42)
#grid = GridSearchCV(SVC(),param_grid=param_grid,cv=cv)
#grid.fit(X,y)
#print("The best parameters are %s with a score of %0.2f" % (grid.best_params_,grid.best_score_))

plt.scatter(X[0:nSegments*nIterations,0],X[0:nSegments*nIterations,1],c='red',label=gestures.keys()[0])
plt.scatter(X[nSegments*nIterations:2*nSegments*nIterations,0],X[nSegments*nIterations:2*nSegments*nIterations,1],c='blue',label=gestures.keys()[1])
plt.scatter(X[2*nSegments*nIterations:3*nSegments*nIterations,0],X[2*nSegments*nIterations:3*nSegments*nIterations,1],c='green',label=gestures.keys()[2])
plt.scatter(X[3*nSegments*nIterations:4*nSegments*nIterations,0],X[3*nSegments*nIterations:4*nSegments*nIterations,1],c='cyan',label=gestures.keys()[3])
plt.scatter(X[4*nSegments*nIterations:5*nSegments*nIterations,0],X[4*nSegments*nIterations:5*nSegments*nIterations,1],c='magenta',label=gestures.keys()[4])
plt.scatter(X[5*nSegments*nIterations:6*nSegments*nIterations,0],X[5*nSegments*nIterations:6*nSegments*nIterations,1],c='lime',label=gestures.keys()[5])
plt.scatter(X[6*nSegments*nIterations:7*nSegments*nIterations,0],X[6*nSegments*nIterations:7*nSegments*nIterations,1],c='orange',label=gestures.keys()[6])
plt.legend(scatterpoints=1,loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

