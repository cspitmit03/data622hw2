#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 13:47:37 2018

@author: cesare
"""


#pull in the data from pull_data.py and train_model.py in order to get files needed and variables
from train_model import *
from pull_data import *

#data review: check for anomalies, missing data etc
pickle_in = open("clf.pkl","rb")
clf = pickle.load(pickle_in)

train_predictions = clf.predict(X)

test_X = cleanup(test)
predictions = clf.predict(test_X)

logger.debug(' ')
logger.debug('The following is the Score Model Results')
logger.debug(classification_report(train["Survived"], train_predictions))

f = open('PulledData.txt','r')
message = f.read()
print(message)
f.close()
