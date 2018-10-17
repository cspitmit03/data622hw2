#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 13:47:37 2018

@author: cesare
"""

from train_model import *
import pickle
import requests
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
from pull_data import *

#data review: check for anomalies, missing data etc
pickle_in = open("clf.pkl","rb")
clf = pickle.load(pickle_in)

train_predictions = clf.predict(X)
# print(classification_report(train["Survived"], train_predictions))

#np.mean(train["Survived"] == train_predictions)

test_X = cleanup(test)
predictions = clf.predict(test_X)

testdf = classification_report(train["Survived"], train_predictions)

logger.debug(' ')
logger.debug('The following is the Score Model Results')
logger.debug(classification_report(train["Survived"], train_predictions))

f = open('PulledData.txt','r')
message = f.read()
print(message)
f.close()
