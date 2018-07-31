#  Copyright 2018 Alvaro Villoslada (Alvipe)
#  This file is part of Open Myo.
#  Open Myo is distributed under a GPL 3.0 license

from emgesture import fextraction as fex
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import pickle

# Data loading
with open("../emg_data/emg_data_20180210-145505.pkl",'r') as fp:
    emg_data = pickle.load(fp)

n_classes = len(emg_data)
n_iterations = [len(value) for value in emg_data.values()][0]
n_channels = 8
n_signals = n_classes*n_iterations*n_channels
emg = list()
segmented_emg = list()
class_labels = list()

#for m in range(1,n_classes+1):
#    for i in range(n_iterations):
#        for c in range(1,n_channels+1):
#            emg.append(emg_data['motion'+str(m)+'_ch'+str(c)][:,i]) #motion1_ch1_i1, motion1_ch2_i1, motion1_ch1_i2, motion1_ch2_i2

for g in emg_data.keys():
    class_labels.append(g)
    for i in range(n_iterations):
        for c in range(n_channels):
            emg.append(np.array(zip(*emg_data[g][i])[c][0:999]))

#for z in range(n_signals):
#    emg[z] = emg[z]*(5/2)/2**24

# Segmentation
for n in range(n_signals):
    segmented_emg.append(fex.segmentation(emg[n],n_samples=50))

# Feature calculation
feature_list = [fex.mav, fex.rms, fex.var, fex.ssi, fex.zc, fex.wl, fex.ssc, fex.wamp]

n_segments = len(segmented_emg[0][0])
n_features = len(feature_list)
feature_matrix = np.zeros((n_classes*n_iterations*n_segments,n_features*n_channels))
n = 0

for i in range(0,n_signals,n_channels):
    for j in range(n_segments):
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
y = fex.generate_target(n_iterations*n_segments,class_labels)

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

plt.scatter(X[0:n_segments*n_iterations,0],X[0:n_segments*n_iterations,1],c='red',label=class_labels[0])
plt.scatter(X[n_segments*n_iterations:2*n_segments*n_iterations,0],X[n_segments*n_iterations:2*n_segments*n_iterations,1],c='blue',label=class_labels[1])
plt.scatter(X[2*n_segments*n_iterations:3*n_segments*n_iterations,0],X[2*n_segments*n_iterations:3*n_segments*n_iterations,1],c='green',label=class_labels[2])
plt.scatter(X[3*n_segments*n_iterations:4*n_segments*n_iterations,0],X[3*n_segments*n_iterations:4*n_segments*n_iterations,1],c='cyan',label=class_labels[3])
plt.scatter(X[4*n_segments*n_iterations:5*n_segments*n_iterations,0],X[4*n_segments*n_iterations:5*n_segments*n_iterations,1],c='magenta',label=class_labels[4])
plt.scatter(X[5*n_segments*n_iterations:6*n_segments*n_iterations,0],X[5*n_segments*n_iterations:6*n_segments*n_iterations,1],c='lime',label=class_labels[5])
plt.scatter(X[6*n_segments*n_iterations:7*n_segments*n_iterations,0],X[6*n_segments*n_iterations:7*n_segments*n_iterations,1],c='orange',label=class_labels[6])
plt.legend(scatterpoints=1,loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
