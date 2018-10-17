#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 13:47:08 2018

@author: cesare
"""

#define function to clean up data


import pickle
import requests
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
from pull_data import *


def cleanup(mydata):
    if {'Survived'}.issubset(mydata.columns):
        mydata = mydata.drop(["Survived"], axis = 1)

    mydata["Embarked"] = mydata["Embarked"].fillna(mydata.Embarked.mode())
    #find mode of embarked data to fill impute missing data.


    # If any ages are null, impute to the age average of the passenger's class and sex
    for i in mydata.Age[mydata.Age.isnull()].index.values:
            pclass = mydata['Pclass'].loc[i] # passenger class of ith null value
            passengersex = mydata['Sex'].loc[i] # passenger class of ith null value
            pclass_mean = np.mean(mydata[(mydata.Pclass == pclass) & (mydata.Sex == passengersex)].Age) # mean age of passenger class & sex
            mydata.loc[i, "Age"] = pclass_mean

    # If any fares are null, impute to the fare average of the passenger's class
    # if sum(mydata.Fare.isnull()) > 0:
    for i in mydata.Fare[mydata.Fare.isnull()].index.values:
        pclass = mydata['Pclass'].loc[i] # passenger class of ith null value
        pclass_mean = np.mean(mydata[mydata.Pclass == pclass].Fare) # mean fare of that passenger class
        mydata.loc[i, "Fare"] = pclass_mean

    # Create Dummy columns for points of Embarkation - S is the base case
    embarked_dummies = pd.get_dummies(mydata["Embarked"])[["C", "Q"]]
    embarked_dummies = embarked_dummies.rename(columns = {"C":"Embark_C",
                       "Q": "Embark_Q"})

    # Create mydata_X, the dataframe that will be returned
    mydata_X = mydata.drop(["Name", "Ticket", "Cabin", "Embarked"], axis = 1)

    # Add Embarked Dummies Columns to X
    mydata_X = mydata_X.assign(**embarked_dummies)

    # Convert Sex Column to dummy, isMale
    mydata_X["isMale"] = mydata_X.Sex == "male"
    mydata_X = mydata_X.drop(["Sex"], axis = 1)

    # No More Nulls left: X.isnull().sum() == 0 for all columns

    return(mydata_X)

y = train["Survived"]
X = cleanup(train)


# Create Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100,
                             max_depth=10,
                             random_state=0,
                             min_samples_split = 3)

# Fit classifier to test data
clf = clf.fit(X, y)

# Save classifier to pickle file, clf.pkl
pickle.dump( clf, open( "clf.pkl", "wb" ) )

PATH='./clf.pkl'

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    logger.debug('File CLF.PKL exists and is readable')
else:
    logger.debug('Either the file CLF.PKL is missing or not readable"')
