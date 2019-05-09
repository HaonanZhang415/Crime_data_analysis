# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 19:18:47 2018

@author: Zhang
"""

import csv
import numpy as np
import time


#start counting
start_time = time.time()

#read in dataset
reader = csv.reader(open("new_main_form.csv", "rt",encoding='utf-8'), delimiter=",")
mainData = list(reader)

Info90 = np.empty((1,22),dtype = 'U10')
Info00 = np.empty((1,22),dtype = 'U10')
Info10 = np.empty((1,22),dtype = 'U10')


for i in range(0,243999):
    for j in range(52,75):
        if mainData[i][j] == '':
            mainData[i][j] = '0'


for i in range(0,243999,21):
    Info90 = mainData[i][52:75]
    Info00 = mainData[i + 10][52:75]
    Info10 = mainData[i + 20][52:75]
    
   
    
    
    
    
    Info90 = [float(i) for i in Info90]
    Info00 = [float(i) for i in Info00]
    Info10 = [float(i) for i in Info10]
    
    firstPart = []
    secondPart = []
    for j in range(0,23):
        firstPart = np.append(firstPart, (Info00[j] - Info90[j])/10)
        secondPart = np.append(secondPart, (Info10[j] - Info00[j])/10)
    
    
    
    for k in range(1,10):
        
        previousNum = [float(ele) for ele in mainData[i + k - 1][52:75]]
        
        result = [x + y for x, y in zip(previousNum, firstPart)]
        mainData[i + k][52:75] = [str(ele) for ele in result]
    
    for k in range(11,20):
        
        previousNum = [float(ele) for ele in mainData[i + k - 1][52:75]]
        result = [x + y for x, y in zip(previousNum, secondPart)]
        mainData[i + k][52:75] = [str(ele) for ele in result]
    
    print('--------------------------------------------')
    percentage = round(i/243999*100,3)
    print('{}%'.format(percentage))



with open("InterpolationResult.csv","w",newline = '') as f:
    writer = csv.writer(f, delimiter = ',')
    writer.writerows(mainData)     


#calculate total running time
elapsed_time = time.time() - start_time

seconds = elapsed_time % 60
minutes = ((elapsed_time - seconds) / 60) % 60
hours = ((elapsed_time - seconds) / 60 - minutes) / 60

print('Total Running time: {}s'.format(round(elapsed_time,2)))
print('Total Running time: {}h {}min {}s'.format(int(hours), int(minutes), round(seconds,2)))   





















