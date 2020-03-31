# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 11:38:04 2020

@author: caghangir
"""

import sys
import socket
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import EEGBCMIMethods as chettoEEG
# %matplotlib qt #plot in new window
import time

class Action:
    
    def __init__(self, run=0, clenchingTime=5, restingTime=2):
       self.run = run
       self.clenchingTime = clenchingTime
       self.restingTime = restingTime
       
       self.initialize_user_interface()
        

       
#       plt.pause(0.03) #update
#       input('Paused, Press enter to continue')
       
    def initialize_user_interface(self):
       # ========= Figure Initialization ==========
       self.fig = plt.figure()
    #           plt.clf()
       figManager = plt.get_current_fig_manager()
       figManager.window.showMaximized()
       plt.axis('off') #remove axis
       
       self.fig.patch.set_facecolor('#000000') #set background color to black 
       
       self.textVar = plt.text(0.4, 0.2, '', fontsize = 500, color="white") 
       # ========= Figure Initialization ==========                 
    
      # ======== Buttons =========
       self.fig.subplots_adjust(bottom=0.2)
         
       axExit = plt.axes([0.25, 0.05, 0.1, 0.05]) #from left-from top, x-axis size, y-axis size
       bExit = Button(axExit, 'Exit')
       bExit.label.set_fontsize(25)
       bExit.on_clicked(self.Exit)
       
       axPause = plt.axes([0.75, 0.05, 0.1, 0.05]) #from left-from top, x-axis size, y-axis size
       bPause = Button(axPause, 'Pause')
       bPause.label.set_fontsize(25)
       bPause.on_clicked(self.Pause)
       
       axBegin = plt.axes([0.05, 0.05, 0.1, 0.05]) #from left-from top, x-axis size, y-axis size
       bBegin = Button(axBegin, 'Begin')
       bBegin.label.set_fontsize(25)
       bBegin.on_clicked(self.Begin)
       # ======== Buttons =========  

    def execution(self):
        
        # plt.gcf().canvas.flush_events()
#        plt.gcf()
        
        sequence = self.sequenceCreation()
        for i in range(len(sequence)):
       
           startTime = time.time()
           if(sequence[i] == '0'):
               self.textVar.set_text('L')
           else:
               self.textVar.set_text('R')  
               
           self.textVar.set_size(500)
           self.textVar.set_position((0.4,0.2))    
           self.textVar.set_color('white')
           
#           plt.show(block=False) #update
#           plt.gcf().canvas.draw_idle()
           self.fig.canvas.draw()
           self.fig.gcf().canvas.flush_events()
#           plt.show(block=False)
#           plt.show(block=False)
           plt.pause(0.03)
           
           time.sleep(self.clenchingTime)
    
           endTime = time.time()
           elapsed_clenchTime = endTime - startTime
           print("Elapsed Clench Time = %s" % elapsed_clenchTime)
           
           startTime = time.time()
           self.textVar.set_text('rest')
           self.textVar.set_size(200)
           self.textVar.set_position((0.35,0.3))
           self.textVar.set_color('blue')
           
#           plt.show(block=False) #update
#           plt.gcf().canvas.draw_idle()
           plt.gcf().canvas.flush_events()
           plt.show(block=False)
           plt.show(block=False)
#           plt.pause(0.03)
           
           time.sleep(self.restingTime)
           
           endTime = time.time()
           elapsed_restTime = endTime - startTime
           print("Elapsed Rest Time = %s" % elapsed_restTime)
    
    #=========== Action =============
    def Exit(self, event):
        sys.exit("Exit button was pressed")
        
    def Begin(self, event):
        self.run = 1
        self.execution()
        
    def Pause(self, event):
#        if(self.run == 0):
#            self.run = 1
#        else:
#            self.run = 0
        input('Paused, Press enter to continue')
    #=========== Action =============

    def sequenceCreation(self):
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
        return sequence
    
    
if __name__ == "__main__":
   print("main")
   callback = Action()
   sequence = callback.sequenceCreation()
   
#   clenchingTime = 5 #seconds
#   restTime = 2 #seconds
#   
#   # ========= Figure Initialization ==========
#   fig = plt.figure()
##           plt.clf()
#   figManager = plt.get_current_fig_manager()
#   figManager.window.showMaximized()
#   plt.axis('off') #remove axis
#   
#   fig.patch.set_facecolor('#000000') #set background color to black 
#   
#   textVar = plt.text(0.4, 0.2, '', fontsize = 500, color="white") 
#   # ========= Figure Initialization ==========                 
#
#  # ======== Buttons =========
#   fig.subplots_adjust(bottom=0.2)
# 
#   axExit = plt.axes([0.25, 0.05, 0.1, 0.05]) #from left-from top, x-axis size, y-axis size
#   bExit = Button(axExit, 'Exit')
#   bExit.label.set_fontsize(25)
#   bExit.on_clicked(callback.Exit)
#   
#   axPause = plt.axes([0.75, 0.05, 0.1, 0.05]) #from left-from top, x-axis size, y-axis size
#   bPause = Button(axPause, 'Pause')
#   bPause.label.set_fontsize(25)
#   bPause.on_clicked(callback.Pause)
#   
#   axBegin = plt.axes([0.05, 0.05, 0.1, 0.05]) #from left-from top, x-axis size, y-axis size
#   bBegin = Button(axBegin, 'Begin')
#   bBegin.label.set_fontsize(25)
#   bBegin.on_clicked(callback.Begin)
#   # ======== Buttons =========        
#   
#   if(callback.run == 1):
#       print("inside")
#   
#   for i in range(len(sequence)):
#       
#       startTime = time.time()
#       if(sequence[i] == '0'):
#           textVar.set_text('L')
#       else:
#           textVar.set_text('R')  
#           
#       textVar.set_size(500)
#       textVar.set_position((0.4,0.2))    
#       textVar.set_color('white')
#       plt.pause(0.03) #update
##       fig.canvas.draw()
#       time.sleep(clenchingTime)
#
#       endTime = time.time()
#       elapsed_clenchTime = endTime - startTime
#       print("Elapsed Clench Time = %s" % elapsed_clenchTime)
#       
#       startTime = time.time()
#       textVar.set_text('rest')
#       textVar.set_size(200)
#       textVar.set_position((0.35,0.3))
#       textVar.set_color('blue')
#       plt.pause(0.03) #update
##       fig.canvas.draw()
#       time.sleep(restTime)
#       
#       endTime = time.time()
#       elapsed_restTime = endTime - startTime
#       print("Elapsed Rest Time = %s" % elapsed_restTime)


   
#   while True:
#       try:
#           textVar.set_text('L') 
#       except Exception as e:
#           print(e)