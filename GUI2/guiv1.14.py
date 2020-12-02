#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 23:17:54 2020

@author: caghangir
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 16:32:49 2020

@author: caghangir
"""

from tkinter import *
from tkinter import font as tkFont
import tkinter.ttk as ttk
from tkinter import Button as Button #tkinter.ttk is also has Button object
import time
import numpy as np
import pickle
import datetime
import os
import sys
import matplotlib.pyplot as plt
# import winsound
# %matplotlib qt
os.chdir('/home/caghangir/Desktop/PhD/LD_BCI/Codes/Lucid-Dream-BCI/GUI2')
#%% =============== Init ===============
class GUI:
    def __init__(self, parentWindow, count=0, clenchingTime=3000, restingTime=2000): #milliseconds
       self.window = parentWindow
       # self.window.rowconfigure(2, weight=1)
       self.count = count
       self.clenchingTime = clenchingTime
       self.restingTime = restingTime
       self.textLogTime = 3000 #milliseconds
       self.initialize_user_interface()
       self.real_log_data = np.empty(shape=[0])
       
       #===== Time Points Initialization ======
       #==== Aligning Process ====
       self.mainIntro = 3 #sec
       self.relaxing = 30 + 1 #sec 1 sec is beep sound
       self.clenchingTeeth = 7 #sec
       self.LRLR = 7 #sec
       self.blink = 6 #sec
       self.finishingBlink = 3 #sec
       #==== Aligning Process ====
       
       self.startClenchingTime = 100 #just start clenching time to give big value for skipping first calculation!
       self.endClenchingTime = 0
       self.startRestingTime = 100
       self.endRestingTime = 0
       
       # self.clenchingTimePoints = np.empty(shape=[0,1]) #time array of clenching initial time points
       # self.restingTimePoints = np.empty(shape=[0,1]) #time array of resting initial time points
       self.allInitialDateTimes = {
           'get ready' : None,
           'relax' : None,
           'clench teeth' : None,
           'perform LRLR' : None,
           'blink' : list(),
           'left' : list(),
           'right' : list(),
           'rest' : list(),
           'finish' : None,
           'all events' : list()
           }
       
       self.allLogData = {
           'real elapsed times' : None,
           'default elapsed times' : None,
           'chosen sequence' : None,
           'elapsed clenching time' : None,
           'elapsed resting time' : None
           }
       #===== Time Points Initialization =====
       
    def initialize_user_interface(self):
        
        #====== Window Initialization =======
        self.window.title("Lucid Dream BCI GUI")
        pad=3
        self.window.geometry("{0}x{1}+0+0".format(self.window.winfo_screenwidth()-pad, self.window.winfo_screenheight()-pad))
        self.window.configure(background='black') #change background color
        #====== Window Initialization =======
        
        # ===== Text Clenching ======
        self.textAction = StringVar()
        self.textAction.set("Begin")
        self.lbl = Label(self.window, textvariable=self.textAction, font=("Arial Bold", 60), foreground='white', background='black')
        self.lbl.place(relx=0.5, rely=0.5, anchor='center')
        # ===== Text Clenching ======
        
        # ===== Text Combobox Clenching Time Interval ======
        self.textComboboxClTiInt = StringVar()
        self.textComboboxClTiInt.set("Clenching Elapsed Time (Sec) :")
        self.lbl2 = Label(self.window, textvariable=self.textComboboxClTiInt, font=("Arial Bold", 10), foreground='white', background='black')
        self.lbl2.place(relx=0.83, rely=0.02, anchor='center')
        # ===== Text Combobox Clenching Time Interval ======
        
        # ===== Text Combobox Resting Time Interval ======
        self.textComboboxRstTiInt = StringVar()
        self.textComboboxRstTiInt.set("Resting Elapsed Time (Sec) :")
        self.lbl3 = Label(self.window, textvariable=self.textComboboxRstTiInt, font=("Arial Bold", 10), foreground='white', background='black')
        self.lbl3.place(relx=0.83, rely=0.055, anchor='center')
        # ===== Text Combobox Resting Time Interval ======
        
        # ====== Text Log =========
        self.textLog = StringVar()
        self.lbl4 = Label(self.window, textvariable=self.textLog, font=("Arial Bold", 20), foreground='white', background='black')
        self.lbl4.place(relx=0.8, rely=0.945, anchor='center')
        # ====== Text Log =========
        
        # ====== Button ===========     
        custom_font = tkFont.Font(family='Helvetica', size=15, weight=tkFont.NORMAL)
        self.btnBegin = Button(self.window, text="Begin", bg="black", fg="white", font=custom_font, command=self.beginClicked)
        self.btnBegin.grid(column=1, row=0)
        self.btnBegin.config(state = DISABLED)
        self.btnPause = Button(self.window, text="Pause", bg="black", fg="white", font=custom_font, command=self.pauseClicked)
        self.btnPause.grid(column=2, row=0)
        self.btnPause.config(state = DISABLED)
        self.btnContinue = Button(self.window, text="Continue", bg="black", fg="white", font=custom_font, command=self.continueClicked)
        self.btnContinue.grid(column=3, row=0)
        self.btnContinue.config(state = DISABLED)
        self.btnExit = Button(self.window, text="Exit", bg="black", fg="white", font=custom_font, command=self.exitClicked)
        self.btnExit.grid(column=4, row=0)
        self.btnReset = Button(self.window, text="Reset", bg="black", fg="white", font=custom_font, command=self.resetClicked)
        self.btnReset.grid(column=5, row=0)
        self.btnReset.config(state = DISABLED)
        self.btnSequenceCreation = Button(self.window, text="Create a Sequence", bg="black", fg="white", \
                                          font=custom_font, command=self.settingSequence)
        self.btnSequenceCreation.place(relx=0, rely=0.07, anchor='w')
        # ====== Button ===========
        
        #===== Combobox Clenching Interval ========
        self.comboClInt = ttk.Combobox(self.window)
        self.comboClInt['values']= (2,3,4,5) #clenching times as second
        self.comboClInt.current(1) #set the selected item
        self.comboClInt.place(relx=0.9, rely=0.01)
        self.comboClInt.bind("<<ComboboxSelected>>", self.changeClenchingInterval)
        #===== Combobox Clenching Interval ========
        
        #===== Combobox Resting Interval ========
        self.comboRestInt = ttk.Combobox(self.window)
        self.comboRestInt['values']= (1,2,3,4,5) #clenching times as second
        self.comboRestInt.current(1) #set the selected item
        self.comboRestInt.place(relx=0.9, rely=0.045)
        self.comboRestInt.bind("<<ComboboxSelected>>", self.changeRestingInterval)
        #===== Combobox Resting Interval ========
        
        # self.window.mainloop()
    
#%% ======== Button Actions ==============        
    def beginClicked(self):
        print('Program is beginning!')
        global doTick
        doTick = True
        
        self.totalLength = len(self.sequence)
        
        self.comboClInt.config(state = DISABLED)
        self.comboRestInt.config(state = DISABLED)
        self.btnBegin.config(state = DISABLED)
        self.btnPause.config(state = NORMAL)
        self.btnReset.config(state = NORMAL)
        
        # self.resting() #init point
        self.aligningTest() #init point
        
    def pauseClicked(self):
        print('Pause Clicked')
        global doTick
        doTick = False
        
        self.btnContinue.config(state = NORMAL)
        self.btnPause.config(state = DISABLED)
        
    def continueClicked(self):
        print('Continue Clicked')
        global doTick
        doTick = True
        
        self.btnContinue.config(state = DISABLED)
        self.btnPause.config(state = NORMAL)
        
        self.resting() #continue point
             
    def exitClicked(self):
        print('Program closed!')
        self.window.quit()
        self.window.destroy()
        
    def resetClicked(self):
              
        #=== Logging ====
        print('Process has stopped!')
        self.textLog.set('Process has stopped!')
        self.lbl4.after(1000, self.log_delete)
        #=== Logging ====
        
        self.window.after(1000, self.restart_program) #fresh restart
        
    def changeClenchingInterval(self, event):
        self.clenchingTime = int(self.comboClInt.get()) * 1000
        
        #==== Logging ====
        print('Clenching interval set as : %s' % self.comboClInt.get())
        self.textLog.set('Clenching Time has Changed to ' + str(int(self.comboClInt.get())) + ' sec!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        #==== Logging ====
        
    def changeRestingInterval(self, event):
        self.restingTime = int(self.comboRestInt.get()) * 1000
        
        #==== Logging ====
        print('Resting interval set as : %s' % self.comboRestInt.get())
        self.textLog.set('Resting Time has Changed to ' + str(int(self.comboRestInt.get())) + ' sec!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        #==== Logging ====
    
    #%% ===== Text Changers =======
    def log_delete(self):
        self.textLog.set('')
        
    def action_text_changer(self, action_type, temp_text):
        self.textAction.set(temp_text)
        self.lbl.place(relx=0.5, rely=0.5, anchor='center')
        
        '''==== Current time Adding ====='''
        current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
        if(action_type == 'blink'):
            self.allInitialDateTimes[action_type].append(current_time)
        else:
            self.allInitialDateTimes[action_type] = current_time
            
        self.allInitialDateTimes['all events'].append(current_time)
        '''==== Current time Adding ====='''
        
        #=== Logging =====
        self.endActionTime = time.time()
        elapsed_action_time = self.endActionTime - self.startActiontime
        print('Elapsed ' + action_type + ': %s' % elapsed_action_time)
        self.real_log_data = np.append(self.real_log_data, elapsed_action_time)
        #=== Logging =====
        
        self.startActiontime = time.time()
        self.startClenchingTime = time.time()
        
    #%% ============== Actions ==================
    def settingSequence(self):
        # self.sequence = self.sequenceCreation()
        self.sequence = pickle.load(open('Sequences/sequence', 'rb')) #82 amount is for all 3 combinations
        self.sequence = self.sequence[0:60] #decrease a bit
        # dateTime = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        # pickle.dump(self.sequence, open('Sequences/' + str(dateTime) ,'wb'))
        
        self.btnBegin.config(state = NORMAL)
        self.btnSequenceCreation.config(state = DISABLED)
        
        #== Logging ===
        print('Sequence Loaded!')
        self.textLog.set('Sequence Loaded!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        #== Logging ===
    
    def restart_program(self):
        print('Program Restarting!')
        self.window.destroy()
        window = Tk()
        callback = GUI(parentWindow=window)
        window.mainloop()
    
    def aligningTest(self):
        
        if not doTick:
            return
        
        self.startActiontime = time.time() # resting() function looks for clenching time so I had to add this one
        self.lbl.config(font=("Arial Bold", 30))
        self.textAction.set('Get Ready!') #3 seconds
        '''==== Current time Adding ====='''
        current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
        self.allInitialDateTimes['get ready'] = current_time
        self.allInitialDateTimes['all events'].append(current_time)
        '''==== Current time Adding ====='''
        
        self.window.after(3000, self.action_text_changer, 'relax', 'Close your eyes and \n relax until beep sound')
        # self.window.after(33000, lambda:winsound.Beep(2500, 1000))
        self.window.after(34000, self.action_text_changer, 'clench teeth', 'Clench your teeth\n as much as possible')
        self.window.after(41000, self.action_text_changer, 'perform LRLR', 'Perform LRLR eye movements\n as much as possible')
        self.window.after(48000, self.action_text_changer, 'blink', 'Blink as much as possible\n 3')
        self.window.after(50000, self.action_text_changer, 'blink', 'Blink as much as possible\n 2')
        self.window.after(52000, self.action_text_changer, 'blink', 'Blink as much as possible\n 1')
       
        self.window.after(54000, lambda:self.resting()) #experiment begin
    
    def clenching(self, actionType):
        
        if not doTick:
            return
        
        #======= Resting Time Calculation =======
        self.endRestingTime = time.time()
        elapsed_restingTime = self.endRestingTime - self.startRestingTime
        self.real_log_data = np.append(self.real_log_data, elapsed_restingTime)
        if(elapsed_restingTime > 0):
            print("Elapsed Resting Time = %s" % elapsed_restingTime)
        #======= Resting Time Calculation =======
      
        if(actionType == '0'):
           self.textAction.set('L')
           self.lbl.place(relx=0.47, rely=0.5, anchor='center')
           
           '''==== Current time Adding ====='''
           current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
           self.allInitialDateTimes['left'].append(current_time)
           self.allInitialDateTimes['all events'].append(current_time)
           '''==== Current time Adding ====='''
           
        else:
           self.textAction.set('R')
           self.lbl.place(relx=0.53, rely=0.5, anchor='center')
           
           '''==== Current time Adding ====='''
           current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
           self.allInitialDateTimes['right'].append(current_time)
           self.allInitialDateTimes['all events'].append(current_time)   
           '''==== Current time Adding ====='''
           
        self.window.update() #window update ne hikmetse ise yaradi!!
        self.count += 1 #next
        
        self.startClenchingTime = time.time()
        self.window.after(self.clenchingTime, self.resting) #do not call method with parameters inside like x(n1,n2)
                                                                                         #this method at first wait than works 
                                                                                         
    def resting(self):
        
        if not doTick:
            return
        
        self.lbl.config(font=("Arial Bold", 60))
        #======= Clenching Time Calculation =====
        self.endClenchingTime = time.time()
        elapsed_clenchingTime = self.endClenchingTime - self.startClenchingTime
        self.real_log_data = np.append(self.real_log_data, elapsed_clenchingTime)
        print("Elapsed Clenching Time = %s" % elapsed_clenchingTime)
        #======= Clenching Time Calculation =====
        
        #======== Resting =======
        self.textAction.set('X')
        self.lbl.place(relx=0.5, rely=0.5, anchor='center')
        
        '''==== Current time Adding ====='''
        current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
        self.allInitialDateTimes['rest'].append(current_time)
        self.allInitialDateTimes['all events'].append(current_time)   
        '''==== Current time Adding ====='''
        
        self.window.update() #window update ne hikmetse ise yaradi!!
        #======== Resting =======
        
        self.startRestingTime = time.time()
        
        #====== If End ========
        if(self.count == self.totalLength):
            self.last_blinks_protocol()
            return
        #====== If End ========
        
        self.window.after(self.restingTime, self.clenching, self.sequence[self.count])
        
    def last_blinks_protocol(self):
        self.textAction.set('Please blink as much as possible')
        self.lbl.place(relx=0.5, rely=0.5, anchor='center')
      
        '''==== Current time Adding ====='''
        current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
        self.allInitialDateTimes['blink'].append(current_time)
        self.allInitialDateTimes['all events'].append(current_time)
        '''==== Current time Adding ====='''
        
        self.startActiontime = time.time()
        self.window.after(3000, self.finish_protocol)
        
    def finish_protocol(self):

        self.textAction.set('The End')
        self.lbl.place(relx=0.5, rely=0.5, anchor='center')
      
        '''==== Current time Adding ====='''
        current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
        self.allInitialDateTimes['finish'] = current_time
        self.allInitialDateTimes['all events'].append(current_time)
        '''==== Current time Adding ====='''        

        self.btnBegin.config(state = NORMAL)
        self.btnPause.config(state = DISABLED)
        self.btnReset.config(state = DISABLED)
        
        #=== Log-data Saving ====
        dateTime = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        
        self.real_log_data = np.append(self.real_log_data, 3) #manually add
                
        '''=========== Save Data ============'''
        default_log_time = np.array([self.mainIntro, self.relaxing, self.clenchingTeeth, self.LRLR, 2, 2, 2])
        for i in range(len(self.sequence)):
            default_log_time = np.append(default_log_time, self.restingTime / 1000)
            default_log_time = np.append(default_log_time, self.clenchingTime / 1000)
        default_log_time = np.append(default_log_time, 3) #blinks
        
        self.allLogData['real elapsed times'] = self.real_log_data
        self.allLogData['default elapsed times'] = default_log_time
        self.allLogData['chosen sequence'] = self.sequence
        self.allLogData['elapsed clenching time'] = self.clenchingTime / 1000
        self.allLogData['elapsed resting time'] = self.restingTime / 1000
       
        #==== Pickle =====
        pickle.dump(self.allLogData, open('Log Data/' + 'allLogData_' + str(dateTime), 'wb'))
        pickle.dump(self.allInitialDateTimes, open('Log Data/' + 'allInitialDateTimes_' + str(dateTime), 'wb'))
        #==== Pickle =====
        '''=========== Save Data ============'''
        
        self.textLog.set('Log Data has been saved into the directory!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        #=== Log-data Saving ====

#%% ======== Pseudo-random Sequence Creation ==========        
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

#%% ========== Main ============        
if __name__ == "__main__":
    window = Tk()
    callback = GUI(parentWindow=window)
    window.mainloop()
#%% ====== Area 51 ===========
# allInitialDateTimes = pickle.load(open('Log Data/' + 'allInitialDateTimes_20-10-15_01-56-28', 'rb'))
# allLogData = pickle.load(open('Log Data/' + 'allLogData_20-10-15_01-56-28', 'rb'))