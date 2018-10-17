#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 12:42:32 2018

@author: cesare
"""

# The following imports the needed packages for this HW Assignment and analysis
import pickle
import requests
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
import csv
import os
import os.path
import io
import requests, csv
import logging
import urllib.request

# Load KAGGLE Credentials
#kaggle credentials are loaded in the API call through the docker file using the JSON download
#the information is stored in the dockerfile for access


payload = {
    '__RequestVerificationToken': '',
    'username': 'cspitmit03',
    'password': 'DCLoyal1',
    'rememberme': 'false'
}

loginURL = 'https://www.kaggle.com/account/login'
dataURL = "https://www.kaggle.com/c/3136/download/train.csv"

with requests.Session() as c:
    response = c.get(loginURL).text
    AFToken = response[response.index('antiForgeryToken')+19:response.index('isAnonymous: ')-12]
    print("AntiForgeryToken={}".format(AFToken))
    payload['__RequestVerificationToken']=AFToken
    c.post(loginURL + "?isModal=true&returnUrl=/", data=payload)
    data = c.get(dataURL)
    with open('train.csv', 'w') as f:
        writer = csv.writer(f)
        reader = csv.reader(data.text.splitlines())

        for row in reader:
            writer.writerow(row)
#    response = c.get(dataURL).content
#    train = pd.read_csv(io.StringIO(response.decode('utf-8')))


dataURL = "https://www.kaggle.com/c/3136/download/test.csv"

with requests.Session() as c:
    response = c.get(loginURL).text
    AFToken = response[response.index('antiForgeryToken')+19:response.index('isAnonymous: ')-12]
    print("AntiForgeryToken={}".format(AFToken))
    payload['__RequestVerificationToken']=AFToken
    c.post(loginURL + "?isModal=true&returnUrl=/", data=payload)
    data = c.get(dataURL)
    with open('test.csv', 'w') as f:
        writer = csv.writer(f)
        reader = csv.reader(data.text.splitlines())

        for row in reader:
            writer.writerow(row)

#with requests.Session() as c:
#    response = c.get(loginURL).text
#    AFToken = response[response.index('antiForgeryToken')+19:response.index('isAnonymous: ')-12]
#    print("AntiForgeryToken={}".format(AFToken))
#    payload['__RequestVerificationToken']=AFToken
#    c.post(loginURL + "?isModal=true&returnUrl=/", data=payload)
#    response = c.get(dataURL).content
#    test = pd.read_csv(io.StringIO(response.decode('utf-8')))



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO) # or any other level
logger.addHandler(ch)

fh = logging.FileHandler('PulledData.txt')
fh.setLevel(logging.DEBUG) # or any level you want
logger.addHandler(fh)

# check to see if files downloaded from kaggle exists
PATH='./train.csv'

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    logger.debug('File TRAIN exists and is readable')
else:
    logger.debug('Either the file TRAIN is missing or not readable')

PATH2='./test.csv'

if os.path.isfile(PATH2) and os.access(PATH2, os.R_OK):
    logger.debug('File TEST exists and is readable')
else:
    logger.debug('Either the file TEST is missing or not readable')

#
train = pd.read_csv('train.csv', index_col = 0)
test = pd.read_csv('test.csv', index_col = 0)

#data review: check for anomalies, missing data etc
train.isnull().sum()
test.isnull().sum()
