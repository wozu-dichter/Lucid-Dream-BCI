# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 15:10:28 2020

@author: caghangir
"""

import numpy as np

pairArray = [['000',0],['001',0],['010',0],['011',0],['100',0],['101',0],['110',0],['111',0]]

sequence = ''
for i in range(10):
    j=0
    while j<8:
        if(i==0 and j==0):
            randPair = np.random.randint(8) #create 1st pair
            sequence += pairArray[randPair][0] #expand sequence
            pairArray[int(sequence,2)][1] += 1 #increase pair count by 1
            j += 1 #process
        else:
            randBinary = np.random.randint(2) # don`t use size=1 which creates array
            tempPair = sequence[-2:] #last 2 letters
            
            tempPair += str(randBinary) 
            tempIndex = int(tempPair,2)
            if(pairArray[tempIndex][1] == i):      
                sequence += str(randBinary) #expand sequence
                pairArray[tempIndex][1] += 1 #increase pair count by 1
                j += 1 #process
            else:
                
                if(randBinary == 0): #Taking binary reverse
                    randBinary=1
                else:
                    randBinary=0
                
                tempPair = sequence[-2:] + str(randBinary)   
                tempIndex = int(tempPair,2)
                if(pairArray[tempIndex] == i):                
                    sequence += str(randBinary) #expand sequence  
                    pairArray[int(tempPair,2)][1] += 1 #increase pair count by 1
                    j += 1 #process
                else: #xy-0, xy-1 are already used so change one of xy randomly!
                    randChoose = np.random.randint(2) + 1
                    randBinary = sequence[-1 * randChoose]
                    sequence = list(sequence)
                    if(randBinary == '0'):
                        sequence[-1 * randChoose] = '1'
                    else:
                        sequence[-1 * randChoose] = '0'
                    sequence = ''.join(sequence)

                    
                    
            
            
            