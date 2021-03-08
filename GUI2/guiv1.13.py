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
        self.allInitialDateTimes[action_type] = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
        
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
        self.sequence = pickle.load(open('Sequences/sequence', 'rb'))
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
        self.window.after(3000, self.action_text_changer, 'get ready', 'Close your eyes and \n relax until beep sound')
        # self.window.after(33000, lambda:winsound.Beep(2500, 1000))
        self.window.after(34000, self.action_text_changer, 'relax', 'Clench your teeth\n as much as possible')
        self.window.after(41000, self.action_text_changer, 'clench teeth', 'Perform LRLR eye movements\n as much as possible')
        self.window.after(48000, self.action_text_changer, 'perform LRLR', 'Blink as much as possible\n 3')
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
           current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
           self.allInitialDateTimes['left'].append(current_time)
           self.allInitialDateTimes['all events'].append(current_time)
        else:
           self.textAction.set('R')
           current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
           self.allInitialDateTimes['right'].append(current_time)
           self.allInitialDateTimes['all events'].append(current_time)   
           
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
        current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
        self.allInitialDateTimes['rest'].append(current_time)
        self.allInitialDateTimes['all events'].append(current_time)   
        self.window.update() #window update ne hikmetse ise yaradi!!
        #======== Resting =======
        
        self.startRestingTime = time.time()
        
        #====== If End ========
        if(self.count == self.totalLength):
            self.finish_protocol()
            return
        #====== If End ========
        
        self.window.after(self.restingTime, self.clenching, self.sequence[self.count])
        
    def finish_protocol(self):
        self.textAction.set('Please blink as much as possible')
        self.startActiontime = time.time()
        # self.window.after(3000, self.textAction.set, 'The End')
        self.window.after(3000, self.action_text_changer, 'finish', 'The End')
        self.btnBegin.config(state = NORMAL)
        self.btnPause.config(state = DISABLED)
        self.btnReset.config(state = DISABLED)
        
        #=== Log-data Saving ====
        dateTime = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        
        self.real_log_data = np.append(self.real_log_data, 3) #manually add
        
        #=== Log-data to EEG data conversion ======
        # default_log_data = self.default_log_data_creator(Fs=500, sequence=self.sequence)
        # dynamic_log_data = self.dynamic_log_data_creator(Fs=500)
        #=== Log-data to EEG data conversion ======
        
        #==== Save Data ====
        default_log_time = np.array([self.mainIntro, self.relaxing, self.clenchingTeeth, self.LRLR, 2, 2, 2])
        for i in range(82):
            default_log_time = np.append(default_log_time, 2)
            default_log_time = np.append(default_log_time, 4)
        default_log_time = np.append(default_log_time, 3) #blinks
        
        #== Pure times session-by-session ====
        pickle.dump(default_log_time, open('Log Data/' + 'default_log_time_' + str(dateTime), 'wb'))
        pickle.dump(self.real_log_data, open('Log Data/' + 'real_log_time_' + str(dateTime), 'wb'))
        print('Pure Times has been saved!')
        #== Pure times session-by-session ====
        
        # pickle.dump(self.real_log_data, open('Log Data/' + 'real_log_data_' + str(dateTime) ,'wb'))
        # pickle.dump(default_log_data, open('Log Data/' + 'default_log_EEG_data_' + str(dateTime) ,'wb'))
        # pickle.dump(dynamic_log_data, open('Log Data/' + 'dynamic_log_EEG_data_' + str(dateTime) ,'wb'))
        # print('EEG reconstructed log data has been saved!')
        #==== Save Data ====
        
        self.textLog.set('Log Data has been saved into the directory!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        #=== Log-data Saving ====
        
        #=== Plot ====
        # plt.plot(default_log_data)
        # plt.plot(dynamic_log_data)
        # plt.title('Log Data')
        # plt.legend(['Default Log Data', 'Real Log Data'])
        #=== Plot ====
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
#%% ============= Log-data to EEG data conversion =========
    def default_log_data_creator(self, Fs, sequence):
        sequence_arr=np.array([int(i) for i in sequence])
        clenching_sec = int(self.clenchingTime/1000)
        resting_sec = int(self.restingTime/1000)
        
        pairing_time = self.mainIntro + self.relaxing + self.clenchingTeeth + self.LRLR + self.blink #sec
        experimental_time = len(sequence) * clenching_sec + len(sequence) * resting_sec #sec
        ending_time = self.finishingBlink #sec
        total_time = int(pairing_time + experimental_time + ending_time) #sec
        log_data = np.zeros((total_time * Fs))
        log_data[0:3*Fs] = 0.5 * np.sin(2 * np.pi * np.arange(self.mainIntro * Fs) / (Fs*3)) + 1 #get ready
        log_data[3*Fs:34*Fs] = np.sin(2 * np.pi * np.arange(self.relaxing * Fs) / (Fs*2)) + 1 #relax
        log_data[34*Fs:41*Fs] = 0.5 * np.sin(2 * np.pi * np.arange(self.clenchingTeeth * Fs) / (Fs/2)) + 1 #LRLR
        log_data[41*Fs:48*Fs] = 0.6 * np.sin(2 * np.pi * np.arange(self.LRLR * Fs) / (Fs/2)) + 0.4 * np.sin(2 * np.pi * np.arange(self.LRLR * Fs) / (Fs*2)) + 1 #Teeth Clench
        log_data[48*Fs:54*Fs] = 0.5 * np.sin(2 * np.pi * np.arange(self.blink * Fs) / (Fs/4)) + 1 #Blink
        onset_points_0 = 54 * Fs + np.where(sequence_arr==0)[0] * Fs * clenching_sec + (np.where(sequence_arr==0)[0] + 1) * Fs * resting_sec #additional gap part for 7 -> 7*200
        onset_points_1 = 54 * Fs + np.where(sequence_arr==1)[0] * Fs * clenching_sec + (np.where(sequence_arr==1)[0] + 1) * Fs * resting_sec
        for i in onset_points_0:
            log_data[i:i+clenching_sec * Fs] = np.ones(clenching_sec * Fs)
        for i in onset_points_1:
            log_data[i:i+clenching_sec * Fs] = np.ones(clenching_sec * Fs) * 2 #multiply with 2 to differentiate visually
        log_data[(total_time - self.finishingBlink) * Fs:] = 0.5 * np.sin(2 * np.pi * np.arange(self.finishingBlink * Fs) / (Fs/4)) + 1 #Last blinks
        
        return log_data
    
    def dynamic_log_data_creator(self, Fs):        
        
        for i in range(1, len(self.real_log_data)):
            self.real_log_data[i] += self.real_log_data[i-1]

        total_time = np.zeros((int(self.real_log_data[-1] * Fs)))
        
        sequence = self.real_log_data * Fs
        sequence = sequence.astype(int)
        
        total_time[0:sequence[0]] = 0.5 * np.sin(2 * np.pi * np.arange(sequence[0]) / (Fs*3)) + 1 #get ready
        total_time[sequence[0]:sequence[1]] = np.sin(2 * np.pi * np.arange(sequence[1]-sequence[0]) / (Fs*2)) + 1 #relax
        total_time[sequence[1]:sequence[2]] = 0.5 * np.sin(2 * np.pi * np.arange(sequence[2]-sequence[1]) / (Fs/2)) + 1 #LRLR
        total_time[sequence[2]:sequence[3]] = 0.6 * np.sin(2 * np.pi * np.arange(sequence[3]-sequence[2]) / (Fs/2)) + 0.4 * np.sin(2 * np.pi * np.arange(sequence[3]-sequence[2]) / (Fs*2)) + 1 #Teeth Clench
        total_time[sequence[3]:sequence[6]] = 0.5 * np.sin(2 * np.pi * np.arange(sequence[6]-sequence[3]) / (Fs/4)) + 1 #Blink
        
        for i in np.arange(8, len(self.real_log_data - 1),2):
            if(sequence[i-8] == 0):
                total_time[sequence[i-1]:sequence[i]] = np.ones(sequence[i]-sequence[i-1])
            else:
                total_time[sequence[i-1]:sequence[i]] = np.ones(sequence[i]-sequence[i-1]) * 2
                
        total_time[sequence[-2]:] = 0.5 * np.sin(2 * np.pi * np.arange(3*Fs) / (Fs/4)) + 1 #Last Blinks
       
        return total_time
#%% ========== Main ============        
if __name__ == "__main__":
    window = Tk()
    callback = GUI(parentWindow=window)
    window.mainloop()
#%% ======= Area 51 =======

#== load log time ===
default_log_time = pickle.load(open('Log Data/default_log_time_20-10-12_20-25-25', 'rb'))
real_log_time = pickle.load(open('Log Data/real_log_time_20-10-12_20-25-25', 'rb'))
plt.plot(np.arange(len(default_log_time)), default_log_time * 1000)
plt.plot(np.arange(len(real_log_time)), real_log_time * 1000)
plt.xlabel('All Events', size=20)
plt.ylabel('Time [Millisecond]', size=20)
plt.legend(['Default Log Time', 'Dynamic Log Time'], loc='upper right', prop={'size':20})

#Difference Calculation
difference = (sum(real_log_time) - sum(default_log_time)) * 1000 #ms
cumulative_differences = (real_log_time - default_log_time) * 1000 #ms
for i in range(1, len(differences_per_event)):
    cumulative_differences[i] += cumulative_differences[i-1]
plt.figure()
plt.plot(cumulative_differences, linewidth=4)
plt.xlabel('All Events', size=20)
plt.ylabel('Cumulative Time Latency [Millisecond]', size=20)

#=== Log-data Creation ====
# default_log_EEG_data = pickle.load(open('Log Data/default_log_EEG_data_20-09-17_17-15-36', 'rb'))
# dynamic_log_EEG_data = pickle.load(open('Log Data/dynamic_log_EEG_data_20-09-17_17-15-36', 'rb'))
# plt.plot(np.linspace(0, len(default_log_EEG_data) / 500, num=len(default_log_EEG_data)), default_log_EEG_data)
# plt.plot(np.linspace(0, len(dynamic_log_EEG_data) / 500, num=len(dynamic_log_EEG_data)), dynamic_log_EEG_data)
# plt.title('Log Data')
# plt.legend(['Default Log Data', 'Dynamic Log Data'], loc='upper right', prop={'size':20})
# plt.xlabel('Time [Second]', size=20)
# plt.ylabel('Unnecessary', size=20)