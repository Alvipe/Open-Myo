#  Copyright 2018 Alvaro Villoslada (Alvipe)
#  This file is part of Open Myo.
#  Open Myo is distributed under a GPL 3.0 license

from sklearn.svm import SVC
from sklearn.externals import joblib

def train(feature_matrix, target):
    classifier = SVC(kernel='rbf',C=100,gamma=1) #C=1e5,gamma=1e-23
    classifier.fit(feature_matrix, target)
    return classifier

def classify(feature_matrix, classifier):
    prediction = classifier.predict(feature_matrix)
    return prediction

def save(classifier):
    joblib.dump(classifier, 'classifier.pkl')
