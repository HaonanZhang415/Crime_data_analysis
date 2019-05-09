# -*- coding: utf-8 -*-
"""
Created on Mon May 28 14:40:25 2018

@author: Zhang
"""

import os,sys
import csv
import numpy as np
import time

from sksurv.linear_model import IPCRidge
from sksurv.metrics import concordance_index_censored
from sksurv.linear_model import CoxPHSurvivalAnalysis

#read in dataset
reader = csv.reader(open("Final_Main_90_01.csv", "rt",encoding='utf-8'), delimiter=",")
mainData = list(reader)
mainData = np.array(mainData[1:96192])

allData = mainData[0:1000,9:16]
indicators = mainData[0:1000,47:48]


#build a boolean indicator
indi = np.full((1000,1),False)

for i in range(0,1000):
    if indicators[i] == '1':
        indi[i] = True
    else:
        indi[i] = False

       
#fill all empty slot with 0s        
for i in range(0,1000):
    for j in range(0,7):
        if allData[i][j] == '':
            allData[i][j] = 0
            
allData = allData.astype('float')

#split the training and test set
trainingData = allData[0:800,0:6]
trainingTarget = allData[0:800,6]
testData = allData[800:1000,0:6]
testTarget = allData[800:1000,6]

#build a structured array by combining indicator and targetValue. It will serve as the target which will be feed into the training algorithm

trainingTargetStruc = np.zeros((800),dtype = [('indicator',bool),('targetValue',float)])
for i in range(0,800):
    trainingTargetStruc[i] = (indi[i],trainingTarget[i])
    
testTargetStruc = np.zeros((200),dtype = [('indicator',bool),('targetValue',float)])
for i in range(0,200):
    testTargetStruc[i] = (indi[800 + i], testTarget[i])



#use the target from kidney survival data

#read in dataset
reader = csv.reader(open("hlaDataAddBloodRace.csv", "rt"), delimiter=",")
x = list(reader)
#remove instances with empty BMI
for row in x[1:20000]:
    if '' in row[:]:
        x.remove(row)

x = np.array(x[1:2001])
#transform race from string to numeric
for i in range(0, 2000):
    j = 3
    if x[i][j]=='WHITE':
        x[i][j] = 1
    if x[i][j]=='BLACK':
        x[i][j] = 2
    if x[i][j]=='NATIVE':
        x[i][j] = 3
    if x[i][j]=='ASIAN':
        x[i][j] = 3
    if x[i][j]=='PACIFIC':
        x[i][j] = 3
    if x[i][j]=='MULTI':
        x[i][j] = 3
    
    j = 14
    if x[i][j]=='WHITE':
        x[i][j] = 1
    if x[i][j]=='BLACK':
        x[i][j] = 2
    if x[i][j]=='NATIVE':
        x[i][j] = 3
    if x[i][j]=='ASIAN':
        x[i][j] = 3
    if x[i][j]=='PACIFIC':
        x[i][j] = 3
    if x[i][j]=='MULTI':
        x[i][j] = 3


#transform blood type from string to numeric
for i in range(0,2000):
    j = 2
    if x[i][j]=='A':
        x[i][j] = 1
    if x[i][j]=='B':
        x[i][j] = 2
    if x[i][j]=='O':
        x[i][j] = 3
    if x[i][j]=='A1':
        x[i][j] = 4
    if x[i][j]=='A2':
        x[i][j] = 5
    if x[i][j]=='AB':
        x[i][j] = 6
    if x[i][j]=='A1B':
        x[i][j] = 7
    if x[i][j]=='A2B':
        x[i][j] = 8
    
    j = 13
    if x[i][j]=='A':
        x[i][j] = 1
    if x[i][j]=='B':
        x[i][j] = 2
    if x[i][j]=='O':
        x[i][j] = 3
    if x[i][j]=='A1':
        x[i][j] = 4
    if x[i][j]=='A2':
        x[i][j] = 5
    if x[i][j]=='AB':
        x[i][j] = 6
    if x[i][j]=='A1B':
        x[i][j] = 7
    if x[i][j]=='A2B':
        x[i][j] = 8
data = x.astype("float")

allTarget = np.zeros((2000),dtype=[('indicator',bool),('time',float)])

for i in range(0,2000):
    if data[i][22] < 0:
        allTarget[i]['time'] = data[i][23]
        allTarget[i]['indicator'] = False
    else:
        allTarget[i]['time'] = data[i][22]
        allTarget[i]['indicator'] = True

trainingTargetKidney = allTarget[0:800]
testTargetKidney = allTarget[800:1000]



estimator = IPCRidge()
estimator.fit(trainingData, trainingTargetKidney)
prediction = estimator.predict(testData)

estimator = CoxPHSurvivalAnalysis()
estimator.fit(trainingData, trainingTargetStruc)
prediction0 = estimator.predict(testData)

result = concordance_index_censored(testTargetStruc["indicator"], testTargetStruc["targetValue"], prediction)
result0 = concordance_index_censored(testTargetStruc["indicator"], testTargetStruc["targetValue"], prediction0)
print(result)
print(prediction)
print(result0)
print(prediction0)



#conclustion: IPCRidge can work on Crime Data!


















