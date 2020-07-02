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

class GUI:
    def __init__(self, parentWindow, count=0, clenchingTime=5000, restingTime=2000): #milliseconds
       self.window = parentWindow
       # self.window.rowconfigure(2, weight=1)
       self.count = count
       self.clenchingTime = clenchingTime
       self.restingTime = restingTime
       self.textLogTime = 3000 #milliseconds
       self.initialize_user_interface()
       
       #===== Time Points Initialization ======
       self.startClenchingTime = 100 #just start clenching time to give big value for skipping first calculation!
       self.endClenchingTime = 0
       self.startRestingTime = 100
       self.endRestingTime = 0
       
       self.clenchingTimePoints = np.empty(shape=[0,1]) #time array of clenching initial time points
       self.restingTimePoints = np.empty(shape=[0,1]) #time array of resting initial time points
       #===== Time Points Initialization ======
       
       os.chdir('C:/Users/caghangir/Desktop/PhD/Research/Lucid Dream BCI/Codes/GUI/Log')
       
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
        self.lbl4.place(relx=0.87, rely=0.945, anchor='center')
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
        self.comboClInt.current(3) #set the selected item
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
    
    # ======= Action =======
    def settingSequence(self):
        self.sequence = self.sequenceCreation()
        dateTime = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        pickle.dump(self.sequence, open('Sequences/' + str(dateTime) ,'wb'))
        
        self.btnBegin.config(state = NORMAL)
        self.btnSequenceCreation.config(state = DISABLED)
        
        #== Logging ===
        print('Sequence Saved!')
        self.textLog.set('Sequence Saved!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        #== Logging ===
#%% ======== Button Actions ==============        
    def beginClicked(self):
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
        global doTick
        doTick = False
        
        self.btnContinue.config(state = NORMAL)
        self.btnPause.config(state = DISABLED)
        
    def continueClicked(self):
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
        print(self.comboClInt.get())
        self.textLog.set('Clenching Time has Changed to ' + str(int(self.comboClInt.get())) + 'sec!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        #==== Logging ====
        
    def changeRestingInterval(self, event):
        self.restingTime = int(self.comboRestInt.get()) * 1000
        
        #==== Logging ====
        print(self.comboRestInt.get())
        self.textLog.set('Resting Time has Changed to ' + str(int(self.comboRestInt.get())) + 'sec!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        #==== Logging ====
    
    #%% ===== Text Changers =======
    def log_delete(self):
        self.textLog.set('')
    # def action_text_changer(self, temp_text):
    #     self.textAction.set(temp_text)
    #%% ======= Actions =======
    def restart_program(self):
        print('Program Restarting!')
        self.window.destroy()
        window = Tk()
        callback = GUI(parentWindow=window)
        window.mainloop()
    
    def aligningTest(self):
        
        if not doTick:
            return
        
        self.textAction.set('Get Ready!') #3 seconds
        self.window.after(3000, self.textAction.set,'Please relax yourself for\n 30 seconds') #30 seconds
        self.window.after(33000, self.textAction.set,'Please perform LRLR eye movements\n as much as possible') #5 seconds
        self.window.after(38000, self.textAction.set,'Please clench your teeth\n as much as possible') #5seconds
        self.window.after(43000, self.textAction.set, 'Please blink \n 3')
        self.window.after(45000, self.textAction.set, 'Please blink \n 2')
        self.window.after(47000, self.textAction.set, 'Please blink \n 1')
        self.window.after(49000, lambda:self.resting()) #experiment begin
    
    def clenching(self, actionType):
        
        if not doTick:
            return
        
        #======= Resting Time Calculation =======
        self.endRestingTime = time.time()
        elapsed_restingTime = self.endRestingTime - self.startRestingTime
        if(elapsed_restingTime > 0):
            print("Elapsed Resting Time = %s" % elapsed_restingTime)
        #======= Resting Time Calculation =======
      
        if(actionType == '0'):
           self.textAction.set('L')
        else:
           self.textAction.set('R')
           
        self.window.update() #window update ne hikmetse ise yaradi!!
        self.count += 1 #next
        
        self.startClenchingTime = time.time()
        self.window.after(self.clenchingTime, self.resting) #do not call method with parameters inside like x(n1,n2)
                                                                                         #this method at first wait than works 
                                                                                         
    def resting(self):
        
        if not doTick:
            return
        
        #======= Clenching Time Calculation =====
        self.endClenchingTime = time.time()
        elapsed_clenchingTime = self.endClenchingTime - self.startClenchingTime
        print("Elapsed Clenching Time = %s" % elapsed_clenchingTime)
        #======= Clenching Time Calculation =====
        
        #======== Resting =======
        self.textAction.set('✕')
        self.window.update() #window update ne hikmetse ise yaradi!!
        #======== Resting =======
        
        self.startRestingTime = time.time()
        
        #====== If End ========
        if(self.count == self.totalLength):
            self.textAction.set('The End')
            self.btnBegin.config(state = ENABLED)
            self.btnPause.config(state = DISABLED)
            self.btnReset.config(state = DISABLED)
            return
        #====== If End ========
        
        self.window.after(self.restingTime, self.clenching, self.sequence[self.count])
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