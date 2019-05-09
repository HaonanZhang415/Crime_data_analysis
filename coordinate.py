# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 20:26:07 2018

@author: Zhang
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 18:58:23 2018

@author: Zhang
"""

import os,sys
import csv
import numpy as np
import time


print("Program started!")

#start counting
start_time = time.time()

#read in dataset
reader = csv.reader(open("Final_Main_90_01.csv", "rt",encoding='utf-8'), delimiter=",")
mainData = list(reader)

mainData = np.array(mainData[1:96192])


    

noMessage = np.zeros((96191,2))
mainData = np.concatenate((mainData,noMessage),axis = 1)


#read in dataset
reader = csv.reader(open("all_fips_lat_long_2015.csv", "rt",encoding='utf-8', errors = 'ignore'), delimiter=",")
lat_long = reader

lat_long = list(lat_long)

lat_long = np.array(lat_long[1:195482])

print('****************TEST BEGIN!*******************')
print(lat_long[0][22])

newForm = np.full((96191,52), fill_value=0, dtype = 'object')

for i in range(0,96191):
    stateFIPS = mainData[i][4]
    placeFIPS = mainData[i][28]
    govType = mainData[i][8]
    govTypeChar = 'A'
    
    if govType == '1':
        govTypeChar = 'H'
    elif govType == '2':
        govTypeChar = 'C'
    elif govType == '3':
        govTypeChar = 'T'
    elif govType == '4':
        govTypeChar = 'A'
        
    govTypeChar = np.str_(govTypeChar)
    
    for j in range(0,195481):
        if stateFIPS == lat_long[j][0]:
            if placeFIPS == lat_long[j][2]:
                if govTypeChar == lat_long[j][22]:
                    newForm[i] = mainData[i]
                    newForm[i][50] = lat_long[j][15]
                    newForm[i][51] = lat_long[j][16]
                    break
                else:
                    newForm[i] = mainData[i]
            else:
                newForm[i] = mainData[i]
        else:
            newForm[i] = mainData[i]
                    
    print('--------------------------------------------')
    percentage = round(i/96191*100,3)
    print('{}%'.format(percentage))
        


#np.savetxt("fll.csv", newForm, fmt='%9s', delimiter=",")

with open("NewFormWithLatLong.csv","w",newline = '') as f:
    writer = csv.writer(f, delimiter = ',')
    writer.writerows(newForm)



                
#calculate total running time
elapsed_time = time.time() - start_time

seconds = elapsed_time % 60
minutes = ((elapsed_time - seconds) / 60) % 60
hours = ((elapsed_time - seconds) / 60 - minutes) / 60

print('Total Running time: {}s'.format(round(elapsed_time,2)))
print('Total Running time: {}h {}min {}s'.format(int(hours), int(minutes), round(seconds,2)))   