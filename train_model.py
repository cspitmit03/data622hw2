#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 13:47:08 2018

@author: cesare
"""

#define function to clean up data

#pull in the data from pull_data.py in order to get files needed and variables
from pull_data import *


def cleanup(datacall):

    # from the isnull check before, we noticed that age, fare, and embarked had missing data that needs to be imputedself.
    #For embarked since it is a categorical data, the mode is being used to fill in the empty info
    #For age and fare, since they are numerical, we can use the mean of subsets to fill in the missing data

    #find mode of embarked data to fill impute missing data.
    if {'Survived'}.issubset(datacall.columns):
        datacall = datacall.drop(["Survived"], axis = 1)


    #The highest mode for embarked is S in both the test and train datasets
    datacall["Embarked"] = datacall["Embarked"].fillna('S')


    for i in datacall.Age[datacall.Age.isnull()].index.values:
            pclass = datacall['Pclass'].loc[i] # passenger class of ith null value
            passengersex = datacall['Sex'].loc[i] # passenger class of ith null value
            pclass_mean = np.mean(datacall[(datacall.Pclass == pclass) & (datacall.Sex == passengersex)].Age) # mean age of passenger class & sex
            datacall.loc[i, "Age"] = pclass_mean

    # If any fares are null, impute to the fare average of the passenger's class
    # if sum(datacall.Fare.isnull()) > 0:
    for i in datacall.Fare[datacall.Fare.isnull()].index.values:
        pclass = datacall['Pclass'].loc[i] # passenger class of ith null value
        pclass_mean = np.mean(datacall[datacall.Pclass == pclass].Fare) # mean fare of that passenger class
        datacall.loc[i, "Fare"] = pclass_mean



    # Create Dummy columns for points of Embarkation
    # from the isna analysis and summary S is the most common value in Embarked column
    embarked_dummies = pd.get_dummies(datacall["Embarked"])[["C", "Q"]]
    embarked_dummies = embarked_dummies.rename(columns = {"C":"Embark_C",
                       "Q": "Embark_Q"})

    # Create datacall_X, the dataframe that will be returned
    datacall_X = datacall.drop(["Name", "Ticket", "Cabin", "Embarked"], axis = 1)

    # Add Embarked Dummies Columns to X
    datacall_X = datacall_X.assign(**embarked_dummies)

    # Convert Sex Column to dummy, isMale
    datacall_X["isMale"] = datacall_X.Sex == "male"
    datacall_X = datacall_X.drop(["Sex"], axis = 1)

    # No More Nulls left: X.isnull().sum() == 0 for all columns

    return(datacall_X)

y = train["Survived"]
X = cleanup(train)


# Create Random Forest Classifier
clf = RandomForestClassifier(n_estimators=50,
                             max_depth=10,
                             random_state=0,
                             min_samples_split = 3)

# Fit classifier to test data
clf = clf.fit(X, y)

# Save classifier to pickle file, myclf.pkl
pickle.dump( clf, open( "myclf.pkl", "wb" ) )

PATH='./myclf.pkl'

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    logger.debug('File CLF.PKL exists and is readable')
else:
    logger.debug('Either the file CLF.PKL is missing or not readable"')
