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
# import serial
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
     
       self.elapsedTimes = {
           'main_intro' : 3000,
           'relaxing' : 31000,
           'beep_sound' : 1000,
           'clench_teeth' : 7000,
           'LRLR' : 7000,
           'blink' : 6000,
           'finish_blink' : 3000,
           'beeping_sound' : 1000
           }
       #==== Aligning Process ====
       
       #==== Aligning Process Free timing =====
       self.elapsedTimes_freetiming = {
           'welcome_session' : 3000,
           'explanation' : 20000,
           'lrlr_sequence_instruction' : 15000,
           'first_free_timing_clench_teeth' : 6000,
           'other_free_timing_clench_teeth' : 4000,
           'long_time' : 60000,
           'long_rest' : 10000,
           'regular_time' : 50000,
           'short_time' : 40000
           }
       #==== Aligning Process Free timing =====
       
       self.startClenchingTime = 100 #just start clenching time to give big value for skipping first calculation!
       self.endClenchingTime = 0
       self.startRestingTime = 100
       self.endRestingTime = 0
       
       self.allInitialDateTimes = {
           'get_ready' : None,
           'relax' : None,
           'clench_teeth' : None,
           'perform_LRLR' : None,
           'blink' : list(),
           'left' : list(),
           'right' : list(),
           'rest' : list(),
           'finish' : None,
           'all_events' : list()
           }
		   
       self.allFreeTimingSessionDateTimes = {
	       'welcome_session' : None,
		   'explanation' : None,
		   'LRLR_sequence_instruction' : None,
		   'free_timing_clench_teeth' : list(), #between each specific time session subject will clench teeth
		   'short_time' : None,
		   'regular_time' : None,
		   'long_time' : None,
		   'long_rest' : list(),
           'finish' : None,
		   'all_events' : list()
	   }
       
       self.allLogData = {
           'real_elapsed_times' : None,
           'default_elapsed_times' : None,
           'chosen_sequence' : None,
           'elapsed_clenching_time' : None,
           'elapsed_resting_time' : None
           }
       
       self.allFreeTimingLogData = {
           'real_elapsed_times' : None,
           'default_elapsed_times' : None,
           'long_clench_session' : None,
           'regular_clench_session' : None,
           'short_clench_session' : None
           }
       #===== Time Points Initialization =====
       
# 	   #====== Serial Port Connection =======
# 	   # serial port stuff
#        PORT_NAME = 'COM1'
#        BAUDRATE  = 115200
#        self.port = serial.Serial(PORT_NAME,baudrate=BAUDRATE)
#        self.BYTEVALUES = {
# 	   'get ready' : bytearray([4]),
# 	   'relax' : bytearray([5]),
# 	   'clench teeth' : bytearray([6]),
# 	   'perform LRLR' : bytearray([7]),
# 	   'blink' : bytearray([8]),
# 	   'finish' : bytearray([9]),
#        'left'  : bytearray([1]),
#        'right' : bytearray([2]),
#        'rest'  : bytearray([3]),
# 	   
# 	   # free timing session events
#        'welcome session' : bytearray([10]),
#        'explanation' : bytearray([11]),
#        'LRLR sequence instruction' : bytearray([12]),
#        'clench time explanation' : bytearray([13]),
#        'free timing clench teeth' : bytearray([14]),
#        'short time' : bytearray([15]),
#        'regular time' : bytearray([16]),
#        'long time' : bytearray([17]),
#        'long rest' : bytearray([18])
# 	   }
#   	   #====== Serial Port Connection =======
	   
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
        self.lbl.config(font=("Arial Bold", 30))
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
		#===== Free timing =====
        self.btnFreeTiming = Button(self.window, text="Free Timing Train", bg="black", fg="white", font=custom_font, \
									command=self.freetimingClicked)
        #self.btnExit.grid(column=6, row=1)
        self.btnFreeTiming.place(relx=0.9, rely=0.9, anchor='w')
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
    
#%% ==================== Button Actions ============================        
    def beginClicked(self):
        print('Program is beginning!')
        global doTick
        doTick = True
        
        self.totalLength = len(self.sequence)
        
        self.comboClInt.config(state = DISABLED)
        self.comboRestInt.config(state = DISABLED)
        self.btnFreeTiming.config(state = DISABLED)
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
    
    def freetimingClicked(self):
	
        global doTick
        doTick = True
              
        self.comboClInt.config(state = DISABLED)
        self.comboRestInt.config(state = DISABLED)
        self.btnBegin.config(state = DISABLED)
        self.btnPause.config(state = DISABLED)
        self.btnReset.config(state = DISABLED)
        self.btnFreeTiming.config(state = DISABLED)
		
        self.startActiontime = time.time() # resting() function looks for clenching time so I had to add this one
        self.lbl.config(font=("Arial Bold", 30))
					
        self.freetimingSession() #begin to the free timing
			
	#==================== Button Actions ============================  

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
    
    #%% ======================== Text Changers ================================
    def log_delete(self):
        self.textLog.set('')
        
    def action_text_changer(self, event_text, textaction, finished_action):
        
        if(event_text == 'blink'):
            self.action_text_event_creator(textaction=textaction, event_text=event_text,\
                                           event_type='normal', append=True, relx=0.5, rely=0.5)
        else:
            self.action_text_event_creator(textaction=textaction, event_text=event_text,\
                                           event_type='normal', append=False, relx=0.5, rely=0.5)
        
        #=== Logging =====
        self.endActionTime = time.time()
        elapsed_action_time = self.endActionTime - self.startActiontime
        print('Elapsed ' + finished_action + ' time: %s' % elapsed_action_time)
        self.real_log_data = np.append(self.real_log_data, elapsed_action_time)
        #=== Logging =====
        
        self.startActiontime = time.time()
        self.startClenchingTime = time.time()
		
    def freetiming_action_text_changer(self, event_text, textaction, finished_action):
     
        if(event_text == 'free_timing_clench_teeth' or event_text == 'long_rest'):
            self.action_text_event_creator(textaction=textaction, event_text=event_text,\
                                           event_type='free_timing', append=True, relx=0.5, rely=0.5)
        else:
            self.action_text_event_creator(textaction=textaction, event_text=event_text,\
                                           event_type='free_timing', append=False, relx=0.5, rely=0.5)
		
		#=== Logging =====
        self.endActionTime = time.time()
        elapsed_action_time = self.endActionTime - self.startActiontime
        print('Elapsed ' + finished_action + ' time: %s' % elapsed_action_time)
        self.real_log_data = np.append(self.real_log_data, elapsed_action_time)
        #=== Logging =====
        
        self.startActiontime = time.time()
		
    #%% ========================= Actions ============================
    
    def settingSequence(self):
        self.sequence = pickle.load(open('Sequences/sequence', 'rb')) #82 amount is for all 3 combinations
        self.sequence = self.sequence[0:60] #decrease a bit
              
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
       
        self.action_text_event_creator(textaction='Get Ready!', event_text='get_ready',\
                                          event_type='normal', append=False, relx=0.5, rely=0.5)
        total_time = self.elapsedTimes['main_intro']
        
        self.window.after(total_time, self.action_text_changer, 'relax', 'Close your eyes and \n relax until beep sound', 'get ready')
        total_time += self.elapsedTimes['relaxing']
        
        # self.window.after(total_time, lambda:winsound.Beep(2500, 1000))
        # total_time += self.elapsedTimes['beep sound']
        self.window.after(total_time, self.action_text_changer, 'clench_teeth', 'Clench your teeth\n as much as possible', 'relax')
        total_time += self.elapsedTimes['clench_teeth']
        
        self.window.after(total_time, self.action_text_changer, 'perform_LRLR', 'Perform LRLR eye movements\n as much as possible', \
                          'clench teech')
        total_time += self.elapsedTimes['LRLR']
        
        self.window.after(total_time, self.action_text_changer, 'blink', 'Blink as much as possible\n 3', 'perform LRLR')
        total_time += int(self.elapsedTimes['blink'] / 3)
        
        self.window.after(total_time, self.action_text_changer, 'blink', 'Blink as much as possible\n 2', 'blink')
        total_time += int(self.elapsedTimes['blink'] / 3)
        
        self.window.after(total_time, self.action_text_changer, 'blink', 'Blink as much as possible\n 1', 'blink')
        total_time += int(self.elapsedTimes['blink'] / 3)
        
        self.window.after(total_time, lambda:self.resting()) #experiment begin
    
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
       
           self.action_text_event_creator(textaction='L', event_text='left',\
                                          event_type='normal', append=True, relx=0.47, rely=0.5)
           
        else:
           
           self.action_text_event_creator(textaction='R', event_text='right',\
                                          event_type='normal', append=True, relx=0.53, rely=0.5)
           
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
        
        self.startRestingTime = time.time()
        
        #====== If End ========
        if(self.count == self.totalLength):
            self.last_blinks_protocol()
            return
        #====== If End ========
        
        #===== Resting =====
        self.action_text_event_creator(textaction='X', event_text='rest',\
                                       event_type='normal', append=True)
        self.window.update() #window update ne hikmetse ise yaradi!!
        
        
        self.window.after(self.restingTime, self.clenching, self.sequence[self.count])
        #===== Resting =====
        
    def last_blinks_protocol(self):
       
        self.action_text_event_creator(textaction='Please blink as much as possible', event_text='blink',\
                                       event_type='normal', append=True)
        
        self.startActiontime = time.time()
        self.window.after(3000, self.finish_protocol)

#%% ========================= Finish Protocols ==================================

    def finish_protocol(self):
        self.action_text_changer(textaction='The End', event_text='finish', finished_action='finished')

        self.btnBegin.config(state = NORMAL)
        self.btnPause.config(state = DISABLED)
        self.btnReset.config(state = DISABLED)
        self.btnFreeTiming.config(state = NORMAL)
        
        #=== Log-data Saving ====
        dateTime = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        
        self.real_log_data = np.append(self.real_log_data, 3) #manually add
                
        '''=========== Save Data ============'''
        default_log_time = np.array([self.elapsedTimes['main_intro'], self.elapsedTimes['relaxing'], self.elapsedTimes['clench_teeth'], \
                                     self.elapsedTimes['LRLR'], int(self.elapsedTimes['blink'] / 3), int(self.elapsedTimes['blink'] / 3), \
                                     int(self.elapsedTimes['blink'] / 3)])
        default_log_time = default_log_time / 1000
            
        for i in range(len(self.sequence)):
            default_log_time = np.append(default_log_time, self.restingTime / 1000)
            default_log_time = np.append(default_log_time, self.clenchingTime / 1000)
        default_log_time = np.append(default_log_time, 3) #blinks
        
        self.allLogData['real_elapsed_times'] = self.real_log_data
        self.allLogData['default_elapsed_times'] = default_log_time
        self.allLogData['chosen_sequence'] = self.sequence
        self.allLogData['elapsed_clenching_time'] = self.clenchingTime / 1000
        self.allLogData['elapsed_resting_time'] = self.restingTime / 1000
       
        #==== Pickle =====
        pickle.dump(self.allLogData, open('Log Data/' + 'allLogData_' + str(dateTime), 'wb'))
        pickle.dump(self.allInitialDateTimes, open('Log Data/' + 'allInitialDateTimes_' + str(dateTime), 'wb'))
        #==== Pickle =====
        '''=========== Save Data ============'''
        
        self.textLog.set('Log Data has been saved into the directory!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        print('Log Data has been saved into the directory!')
        #=== Log-data Saving ====

    def freetiming_finish_protocol(self):
        
        self.freetiming_action_text_changer(textaction='The End', event_text='finish', finished_action='finished')
    
        self.btnBegin.config(state = NORMAL)
        self.btnFreeTiming.config(state = NORMAL)
        self.btnPause.config(state = DISABLED)
        self.btnReset.config(state = DISABLED)
        
        '''============== Log-data Saving =================='''
        dateTime = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
                       
        '''=========== Save Data ============'''
        default_log_time = np.array([self.elapsedTimes_freetiming['welcome_session'], self.elapsedTimes_freetiming['explanation'],\
                                     self.elapsedTimes_freetiming['lrlr_sequence_instruction'], \
                                     self.elapsedTimes_freetiming['first_free_timing_clench_teeth'], \
                                     self.elapsedTimes_freetiming['long_time'], \
                                     self.elapsedTimes_freetiming['long_rest'], \
                                     self.elapsedTimes_freetiming['other_free_timing_clench_teeth'], \
                                     self.elapsedTimes_freetiming['regular_time'], \
                                     self.elapsedTimes_freetiming['long_rest'], \
                                     self.elapsedTimes_freetiming['other_free_timing_clench_teeth'], \
                                     self.elapsedTimes_freetiming['short_time'], \
                                     self.elapsedTimes_freetiming['other_free_timing_clench_teeth']])
        default_log_time = default_log_time / 1000
       
        self.allFreeTimingLogData['real_elapsed_times'] = self.real_log_data
        self.allFreeTimingLogData['default_elapsed_times'] = default_log_time
       
        self.allFreeTimingLogData['long_clench_session'] = self.allFreeTimingLogData['real_elapsed_times'][4]
        self.allFreeTimingLogData['regular_clench_session'] = self.allFreeTimingLogData['real_elapsed_times'][7]
        self.allFreeTimingLogData['short_clench_session'] = self.allFreeTimingLogData['real_elapsed_times'][10]
        
        #==== Pickle =====
        pickle.dump(self.allFreeTimingLogData, open('Log Data/' + 'allFreeTimingLogData_' + str(dateTime), 'wb'))
        pickle.dump(self.allFreeTimingSessionDateTimes, open('Log Data/' + 'allFreeTimingSessionDateTimes_' + str(dateTime), 'wb'))
        #==== Pickle =====
        '''=========== Save Data ============'''
        
        self.textLog.set('Log Data has been saved into the directory!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        print('Log Data has been saved into the directory!')
        '''============== Log-data Saving =================='''
    
		
#%% ==================================== Free Timing Session ============================================
    def freetimingSession(self):
        
      	#=== Logging ====
        print('Free timing session activated')
        self.textLog.set('Free timing session activated!')
        self.lbl4.after(1000, self.log_delete)
		#=== Logging ====
        
        self.action_text_event_creator(textaction='Welcome to the Free Timing Session', event_text='welcome_session',\
                                       event_type='free_timing', append=False)
            
        total_time = self.elapsedTimes_freetiming['welcome_session']
        self.window.after(total_time, self.freetiming_action_text_changer,\
                          'explanation', 'In this session, you will freely clench your hands in specific order without time limitation\n' + \
                          'You will have 3 different sub-sessions.\n\n' + \
                          '* In 1st sub-session, you will clench your hands slowly\n' + \
                          '                    * In 2nd sub-session, you will clench your hands in a normal period of time\n' + \
                          '* In 3rd sub-session, you will clench your hands faster\n' + \
                          '\nTimes are perceptual for you and you have your own long, normal or short period of time\n' + \
                          'for clenching tasks. So, decide your own time length', 'welcome session') #20 sec
        total_time += self.elapsedTimes_freetiming['explanation']
        
        self.window.after(total_time, self.freetiming_action_text_changer,\
                          'LRLR_sequence_instruction', 'Begin to lench your left hand and right hand in a loop for 4 times\n' +
                          ' and you will perform clenches 8 times in total as LRLRLRLR', 'explanation') #15 sec
        total_time += self.elapsedTimes_freetiming['lrlr_sequence_instruction']
        
        self.window.after(total_time, self.freetiming_action_text_changer,\
                          'free_timing_clench_teeth', 'Clench Your Teeth', 'LRLR sequence instruction') #6 sec
        total_time += self.elapsedTimes_freetiming['first_free_timing_clench_teeth']
        
        self.window.after(total_time, self.freetiming_action_text_changer,\
                          'long_time', 'Clench your hands slowly for 8 times\n\n' + 'LRLRLRLR', 'free timing clench teeth') #60 sec
        total_time += self.elapsedTimes_freetiming['long_time']
        
        self.window.after(total_time, self.freetiming_action_text_changer,\
                          'long_rest', 'Rest', 'long time clenching session') # 10 sec
        total_time += self.elapsedTimes_freetiming['long_rest']
        
        self.window.after(total_time, self.freetiming_action_text_changer,\
                          'free_timing_clench_teeth', 'Clench Your Teeth', 'long rest') #4 sec
        total_time += self.elapsedTimes_freetiming['other_free_timing_clench_teeth']
        
        self.window.after(total_time, self.freetiming_action_text_changer,\
                          'regular_time', 'Clench your hands in regular speed for 8 times\n\n' + 'LRLRLRLR', 'free timing clench teeth') #50 sec
        total_time += self.elapsedTimes_freetiming['regular_time']
        
        self.window.after(total_time, self.freetiming_action_text_changer,\
                          'long_rest', 'Rest', 'regular time clenching session') # 10 sec
        total_time += self.elapsedTimes_freetiming['long_rest']
        
        self.window.after(total_time, self.freetiming_action_text_changer,\
                          'free_timing_clench_teeth', 'Clench Your Teeth', 'long rest') #4 sec
        total_time += self.elapsedTimes_freetiming['other_free_timing_clench_teeth']
        
        self.window.after(total_time, self.freetiming_action_text_changer,\
                          'short_time', 'Clench your hands fastly for 8 times\n\n' + 'LRLRLRLR', 'free timing clench teeth') #40 sec
        total_time += self.elapsedTimes_freetiming['short_time']
        
        self.window.after(total_time, self.freetiming_action_text_changer,\
                          'free_timing_clench_teeth', 'Clench Your Teeth', 'short time clenching session') #4 sec
        total_time += self.elapsedTimes_freetiming['other_free_timing_clench_teeth']
        
        self.window.after(total_time, self.freetiming_finish_protocol) #finishing protocol activated
            
#%% ============================= Special Functions ======================
    def action_text_event_creator(self, textaction, event_text, event_type='normal', append=False, relx=0.5, rely=0.5):
        self.textAction.set(textaction)
        self.lbl.place(relx=relx, rely=rely, anchor='center')
        # self.port.write(self.BYTEVALUES[event_text]) #stimulus
        
        current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]
        
        if(event_type == 'normal'):
            
            '''==== Current time Adding ====='''
            if(append==True):
                self.allInitialDateTimes[event_text].append(current_time)
            else:
                self.allInitialDateTimes[event_text] = current_time
                
            self.allInitialDateTimes['all_events'].append(current_time)
            '''==== Current time Adding ====='''
            
        elif(event_type == 'free_timing'):
            
            '''==== Current time Adding ====='''
            if(append==True):
                self.allFreeTimingSessionDateTimes[event_text].append(current_time)
            else:
                self.allFreeTimingSessionDateTimes[event_text] = current_time
                
            self.allFreeTimingSessionDateTimes['all_events'].append(current_time)
            '''==== Current time Adding ====='''

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
# allInitialDateTimes_free = pickle.load(open('Log Data/' + 'allFreeTimingSessionDateTimes_20-10-20_15-21-17', 'rb'))
# allLogData_free = pickle.load(open('Log Data/' + 'allFreeTimingLogData_20-10-20_15-21-17', 'rb'))

# allInitialDateTimes = pickle.load(open('Log Data/' + 'allInitialDateTimes_20-10-20_17-32-23', 'rb'))
# allLogData = pickle.load(open('Log Data/' + 'allLogData_20-10-20_17-32-23', 'rb'))