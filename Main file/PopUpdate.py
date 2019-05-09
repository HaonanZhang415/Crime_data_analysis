# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 20:56:40 2018

@author: Zhang
"""

import csv
import numpy as np
import time


#start counting
start_time = time.time()

#read in dataset
reader = csv.reader(open("NewFormWithLatLong.csv", "rt",encoding='utf-8'), delimiter=",")
mainData = list(reader)

mainData = np.array(mainData[1:96192])


noMessage = np.zeros((96191,23))
mainData = np.concatenate((mainData,noMessage),axis = 1)


#read in population info
reader = csv.reader(open("Census_1990_Form.csv", "rt",encoding='utf-8'), delimiter=",")
pop1990 = list(reader)
pop1990 = np.array(pop1990[1:90836])

reader = csv.reader(open("Census_2000_Form_Finished_County.csv", "rt",encoding='utf-8'), delimiter=",")
pop2000 = list(reader)
pop2000 = np.array(pop2000[1:90836])

reader = csv.reader(open("Census_2010_Form_Finished_County.csv", "rt",encoding='utf-8'), delimiter=",")
pop2010 = list(reader)
pop2010 = np.array(pop2010[1:90836])

years = ['1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010']
#build a complete form!



k = 0
previousFIPS = '3000'
newMainForm = np.empty((320063,75),dtype = 'U10')
n = 0


for i in range(0,96191):
    placeFIPS = mainData[i][28]
    
    if placeFIPS == previousFIPS:
        
        if n == 21:
            print(i)
        
        
        
        
        if mainData[i][2] == years[n]:
            newMainForm[k] = mainData[i]
            k += 1
            n += 1
            continue
        else:
            newMainForm[k][0:2] = mainData[i-1][0:2]
            newMainForm[k][3:6] = mainData[i-1][3:6]
            newMainForm[k][8] = mainData[i-1][8]
            newMainForm[k][11] = mainData[i-1][11]
            newMainForm[k][28:30] = mainData[i-1][28:30]
            newMainForm[k][50:52] = mainData[i-1][50:52]
            newMainForm[k][2] = years[n]
            k += 1
            n += 1
    
    else:
#        
        
        for m in range(0,20):
            if newMainForm[k-1][2] == years[m]:
                newMainForm[k][0:2] = mainData[i-1][0:2]
                newMainForm[k][3:6] = mainData[i-1][3:6]
                newMainForm[k][8] = mainData[i-1][8]
                newMainForm[k][11] = mainData[i-1][11]
                newMainForm[k][28:30] = mainData[i-1][28:30]
                newMainForm[k][50:52] = mainData[i-1][50:52]
                newMainForm[k][2] = years[m + 1]
                k += 1
    
        if mainData[i][2] == '1990':
            newMainForm[k] = mainData[i]
            previousFIPS = mainData[i][28]
            k += 1
            n = 1
            continue
        
        else:
            for x in range(0,21):
                if years[x] != mainData[i][2]:
                    newMainForm[k][0:2] = mainData[i][0:2]
                    newMainForm[k][3:6] = mainData[i][3:6]
                    newMainForm[k][8] = mainData[i][8]
                    newMainForm[k][11] = mainData[i][11]
                    newMainForm[k][28:30] = mainData[i][28:30]
                    newMainForm[k][50:52] = mainData[i][50:52]
                    newMainForm[k][2] = years[x]
                    k += 1
                else:
                    newMainForm[k] = mainData[i]
                    previousFIPS = mainData[i][28]
                    k += 1
                    n = x + 1
                    break
            
            
            
            
            
            
        
with open("new_main_form_without_pop.csv","w",newline = '') as f:
    writer = csv.writer(f, delimiter = ',')
    writer.writerows(newMainForm)       












print('New form created!')

#start merging!


for i in range(0,90835):
    if pop1990[i][4][0] =='0':
        pop1990[i][4] = pop1990[i][4][1:]
        
    if pop2000[i][4][0] == '0':
        pop2000[i][4] = pop2000[i][4][1:]

    if pop1990[i][1][0:2] == '00':
        pop1990[i][1] = pop1990[i][1][2:]
    if pop1990[i][1][0] == '0':
        pop1990[i][1] = pop1990[i][1][1:]
    

    if pop2000[i][1][0:2] == '00':
        pop2000[i][1] = pop2000[i][1][2:]
    if pop2000[i][1][0] == '0':
        pop2000[i][1] = pop2000[i][1][1:]






for i in range(0,244000):
    stateFIPS = newMainForm[i][4]
    placeFIPS = newMainForm[i][28]
    year = newMainForm[i][2]
    
    if year == '1990':
        for j in range(0,90835):
            if stateFIPS == pop1990[j][4] and placeFIPS == pop1990[j][1]:
                newMainForm[i][52:75] = pop1990[j][5:28]
                break
                 
    elif year == '2000':
        for j in range(0,90835):
            if stateFIPS == pop2000[j][4] and placeFIPS == pop2000[j][1]:
                newMainForm[i][52:75] = pop2000[j][5:28]
                break
                
    elif year == '2010':
        for j in range(0,90835):
            if stateFIPS == pop2010[j][4] and placeFIPS == pop2010[j][1]:
                newMainForm[i][52:75] = pop2010[j][5:28]
                break
                
                
    else:
        continue
    
    print('--------------------------------------------')
    percentage = round(i/244000*100,3)
    print('{}%'.format(percentage))





with open("new_main_form.csv","w",newline = '') as f:
    writer = csv.writer(f, delimiter = ',')
    writer.writerows(newMainForm)



#calculate total running time
elapsed_time = time.time() - start_time

seconds = elapsed_time % 60
minutes = ((elapsed_time - seconds) / 60) % 60
hours = ((elapsed_time - seconds) / 60 - minutes) / 60

print('Total Running time: {}s'.format(round(elapsed_time,2)))
print('Total Running time: {}h {}min {}s'.format(int(hours), int(minutes), round(seconds,2)))   




















