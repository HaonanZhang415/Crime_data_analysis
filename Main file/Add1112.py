# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 23:46:39 2018

@author: Zhang
"""

import csv
import numpy as np
import time


#start counting
start_time = time.time()

#read in dataset
reader = csv.reader(open("InterpolationResult.csv", "rt",encoding='utf-8'), delimiter=",")
mainData = list(reader)

mainData = np.array(mainData)


newMainForm = np.empty((255617,75),dtype = 'U10')
previousFIPS = '3000'
k = 0
for i in range(0,243999):
    if mainData[i][28] == previousFIPS:
        newMainForm[k] = mainData[i]
        k += 1
    else:
        newMainForm[k][2] = '2011'
        newMainForm[k][0:2] = mainData[i-1][0:2]
        newMainForm[k][3:6] = mainData[i-1][3:6]
        newMainForm[k][8] = mainData[i-1][8]
        newMainForm[k][11] = mainData[i-1][11]
        newMainForm[k][28:30] = mainData[i-1][28:30]
        newMainForm[k][50:52] = mainData[i-1][50:52]
        
        
        newMainForm[k + 1][2] = '2012'
        newMainForm[k + 1][0:2] = mainData[i-1][0:2]
        newMainForm[k + 1][3:6] = mainData[i-1][3:6]
        newMainForm[k + 1][8] = mainData[i-1][8]
        newMainForm[k + 1][11] = mainData[i-1][11]
        newMainForm[k + 1][28:30] = mainData[i-1][28:30]
        newMainForm[k + 1][50:52] = mainData[i-1][50:52]
        
        previousFIPS = mainData[i][28]
        k += 2
        
        print('--------------------------------------------')
        percentage = round(i/243999*100,3)
        print('{}%'.format(percentage))
        
newMainForm[255615][2] = '2011'
newMainForm[255615][0:2] = newMainForm[255614][0:2]
newMainForm[255615][3:6] = newMainForm[255614][3:6]
newMainForm[255615][8] = newMainForm[255614][8]
newMainForm[255615][11] = newMainForm[255614][11]
newMainForm[255615][28:30] = newMainForm[255614][28:30]
newMainForm[255615][50:52] = newMainForm[255614][50:52]


newMainForm[255616][2] = '2012'
newMainForm[255616][0:2] = newMainForm[255614][0:2]
newMainForm[255616][3:6] = newMainForm[255614][3:6]
newMainForm[255616][8] = newMainForm[255614][8]
newMainForm[255616][11] = newMainForm[255614][11]
newMainForm[255616][28:30] = newMainForm[255614][28:30]
newMainForm[255616][50:52] = newMainForm[255614][50:52]
print('First mission completed!')
        
Info00 = np.empty((1,22),dtype = 'U10')
Info10 = np.empty((1,22),dtype = 'U10')

for i in range(0,255617):
    for j in range(52,75):
        if newMainForm[i][j] == '':
            newMainForm[i][j] = '0'


for i in range(0,255617,23):
    Info00 = newMainForm[i + 10][52:75]
    Info10 = newMainForm[i + 20][52:75]
    
    Info00 = [float(i) for i in Info00]
    Info10 = [float(i) for i in Info10]
    
    secondPart = []
    for j in range(0,23):
        secondPart = np.append(secondPart, (Info10[j] - Info00[j])/10)
    
    
    for k in range(21,23):
        previousNum = [float(ele) for ele in newMainForm[i + k - 1][52:75]]
        result = [x + y for x, y in zip(previousNum, secondPart)]
        newMainForm[i + k][52:75] = [str(ele) for ele in result]
    
    
    
    
    
    
with open("InterpolationResult1112.csv","w",newline = '') as f:
    writer = csv.writer(f, delimiter = ',')
    writer.writerows(newMainForm)     


#calculate total running time
elapsed_time = time.time() - start_time

seconds = elapsed_time % 60
minutes = ((elapsed_time - seconds) / 60) % 60
hours = ((elapsed_time - seconds) / 60 - minutes) / 60

print('Total Running time: {}s'.format(round(elapsed_time,2)))
print('Total Running time: {}h {}min {}s'.format(int(hours), int(minutes), round(seconds,2)))      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    