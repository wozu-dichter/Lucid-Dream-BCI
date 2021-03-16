
import tkinter as tk 
from tkinter import ttk 
from tkinter import *
from tkinter import font as tkFont
from PIL import ImageTk, Image
import serial

import time
import numpy as np
import pickle
import datetime
import os
import sys
import matplotlib.pyplot as plt

import pygame
import winsound
import tkvideo

abspath = os.path.abspath(sys.argv[0]) 
dname = os.path.dirname(abspath) #Absoulute directory location where this script is located!
os.chdir(dname)
current_dir = os.getcwd()

# os.system('python audiovisualization.py')
# exec(open("audiovisualization.py").read())
# import subprocess
# # subprocess.run("python audiovisualization.py", shell=True)
# subprocess.call("python audiovisualization.py", shell=True)

LARGEFONT =("Verdana", 35) 
   
class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):  
          
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs) 
        
        pad=3
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth()-pad, self.winfo_screenheight()-pad))
        
        #===== Proportional Width/Height =========
        print("============")
        print("Current Screen width : %d" % self.winfo_screenwidth())
        print("Current Screen height : %d" % self.winfo_screenheight())
        print("============")
        self.total_width = self.winfo_screenwidth()
        self.total_height = self.winfo_screenheight()
        #===== Proportional Width/Height =========
        
        # creating a container 
        container = tk.Frame(self)   
        container.pack(side = "top", fill = "both", expand = True)  
   
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 
		
		#port connection
        PORT_NAME = 'COM1'
        BAUDRATE  = 115200
        #self.port = 1152000
        #self.port = serial.Serial(PORT_NAME,baudrate=BAUDRATE)
   
        # initializing frames to an empty array 
        self.frames = {}   
   
        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (StartPage, DreamBCI, DreamSpeech, LucidityInduction, MusicandSleep): 
   
            frame = F(container, self) 
   
            # initializing frame of that object from 
            # startpage, page1, page2 respectively with  
            # for loop 
            self.frames[F] = frame  
   
            frame.grid(row = 0, column = 0, sticky ="nsew") 
   
        self.show_frame(StartPage) 
   
    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise() 
        
    def exit(self):
        print('Program closed!')
        self.quit()
        self.destroy()
        
    def restart_dreamBCI(self):
        print('BCI Program is restarting!')
        self.quit()
        self.destroy()
        
        app = tkinterApp() 
        app.mainloop() 
        self.show_frame(DreamBCI)
        
    def restart_dreamSpeech(self):
        print('Program is restarting!')
        self.quit()
        self.destroy()
        
        app = tkinterApp() 
        app.mainloop() 
        self.show_frame(DreamSpeech)
        
# first window frame startpage 
   
class StartPage(tk.Frame): 
    
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 
          
        self.config(background='black')
        self.controller = controller
        self.window = parent
        
        total_width = self.controller.total_width
        total_height = self.controller.total_height
        
        # label of frame Layout 2 
        label = tk.Label(self, text ="Meta-Communication with Dreamers", font = LARGEFONT, bg="black", fg="white") 
        label.config(font=("Arial Bold", 30))
        
        # putting the grid in its place by using 
        # grid 
        # label.grid(row = 0, column = 1, padx = 250, pady = 20)  
        label.place(x=total_width/4, y=int(total_height * 0.0057), width=total_width/2, height=total_height * 0.115)
       
        my_label = tk.Label(self)
        my_label.place(x=total_width/3, y=total_height * 0.115, width=total_width/3, height=total_height * 0.4)
        player = tkvideo.tkvideo("Media/thematrix_knockknock.mp4", my_label, loop = 1, size = (888,500))
        player.play()
        
        
        btnDreamBCI = tk.Button(self, text ="Dream BCI", command = lambda : controller.show_frame(DreamBCI), \
                                bg="black", fg="white", width = 50, height = 3, font=20) 
        btnDreamBCI.place(x=total_width/4.5, y=total_height * 0.55, width=total_width/2, height=total_height * 0.069)
   
        btnSpeech = tk.Button(self, text ="Dream Speech Recognition", command = lambda : controller.show_frame(DreamSpeech), \
                              bg="black", fg="white", width = 50, height = 3, font=20) 
        btnSpeech.place(x=total_width/4.5, y=total_height * 0.65, width=total_width/2, height=total_height * 0.069)
   
        btnLucidityInduction = tk.Button(self, text ="Lucidity Induction", command = lambda : controller.show_frame(LucidityInduction), \
                                bg="black", fg="white", width = 50, height = 1, font=20) 
        btnLucidityInduction.place(x=total_width/4.5, y=total_height * 0.75, width=total_width/2, height=total_height * 0.069)     
   
        btnExit = tk.Button(self, text ="Exit", command = lambda : controller.exit(), \
                            bg="black", fg="white", width = 50, height = 3, font=20) 
        btnExit.place(x=total_width/4.5, y=total_height * 0.85, width=total_width/2, height=total_height * 0.069)
        
        btnMusicandSleep = tk.Button(self, text ="Music and Sleep", command = lambda : controller.show_frame(MusicandSleep), \
						bg="black", fg="white", width = 15, height = 3, font=15) 
        btnMusicandSleep.place(x=total_width * 0.032, y=total_height * 0.23, width=total_width * 0.26, height=total_height * 0.069)
        
		#===== Additional Buttons =========
        btnBaselineCheck = tk.Button(self, text ="Baseline Check", command = lambda : self.baseline_checking(), \
						bg="black", fg="white", width = 20, height = 3, font=15) 
        btnBaselineCheck.place(x=total_width * 0.78 , y=total_height * 0.11, width=total_width * 0.19, height=total_height * 0.069)
        
        btnBaselineCheck_beforesleep = tk.Button(self, text ="Baseline Check Before Sleep", command = lambda : self.baseline_checking_before_sleep(), \
						bg="black", fg="white", width = 20, height = 3, font=15) 
        btnBaselineCheck_beforesleep.place(x=total_width * 0.78 , y=total_height * 0.2, width=total_width * 0.19, height=total_height * 0.069)
		
        btnMotivationalSpeech_dreamBCI = tk.Button(self, text ="Motivational Speech Dream BCI", command = lambda : self.motivational_speech_LDBCI(), \
						bg="black", fg="white", width = 28, height = 3, font=20) 
        btnMotivationalSpeech_dreamBCI.place(x=total_width * 0.75, y=total_height * 0.462, width=total_width * 0.24, height=total_height * 0.069)
		
        btnMotivationalSpeech_dreamSpeech = tk.Button(self, text ="Motivational Speech Dream Speech", command = lambda : self.motivational_speech_dreamSpeech(), \
						bg="black", fg="white", width = 28, height = 3, font=20) 
        btnMotivationalSpeech_dreamSpeech.place(x=total_width * 0.75, y=total_height * 0.577, width=total_width * 0.24, height=total_height * 0.069)
		#===== Additional Buttons =========
        
        #=== Port connection ====
        PORT_NAME = 'COM2'
        BAUDRATE  = 115200
        #self.port2 = serial.Serial(PORT_NAME,baudrate=BAUDRATE)
		#=== Port connection ====
        
    def baseline_checking(self):
		
       self.baseline_events = {
	   'close_your_eyes' : bytearray([50]),
	   'open_your_eyes' : bytearray([51]),
       'clench_teeth' : bytearray([52]),
       'LRLR' : bytearray([53]),
       'eye_blinks' : bytearray([54]),
	   'finish' : bytearray([55])
       }
       
       self.baseline_check_time = { #absolute time of baseline check .wav
       'closeyoureyes' : 3000,
       'openyoureyes' : 27000,
       'clenchyourteeth' : 46000,
       'doLRLR' : 65000,
       'blink' : 78000,
       'again_clenchyourteeth' : 94000,
       'again_doLRLR' : 109000,
       'again_blink' : 122000,
       'finish' : 136000
       }
	   
       os.chdir(current_dir + '\\Audio')
       
       pygame.init()
       pygame.mixer.init()
       pygame.mixer.music.load('baseline_check.wav')
       pygame.mixer.music.play()
       
       baseline_check_time = self.baseline_check_time['closeyoureyes']
        # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events['close_your_eyes'])))
       
       baseline_check_time = self.baseline_check_time['openyoureyes']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events['open_your_eyes'])))

       baseline_check_time = self.baseline_check_time['clenchyourteeth']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events['clench_teeth'])))
       
       baseline_check_time = self.baseline_check_time['doLRLR']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events['LRLR'])))
       
       baseline_check_time = self.baseline_check_time['blink']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events['eye_blinks'])))
       
       baseline_check_time = self.baseline_check_time['again_clenchyourteeth']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events['clench_teeth'])))
       
       baseline_check_time = self.baseline_check_time['again_doLRLR']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events['LRLR'])))
       
       baseline_check_time = self.baseline_check_time['again_blink']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events['eye_blinks'])))
       
       baseline_check_time = self.baseline_check_time['finish']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events['finish'])))
		
    def baseline_checking_before_sleep(self):
		
       self.baseline_events_before_sleep = {
	   'look_totheceiling_eyesopen' : bytearray([50]),
	   'look_totheceiling_eyesclosed' : bytearray([51]),
       'clench_teeth' : bytearray([52]),
       'LRLR' : bytearray([53]),
       'eye_blinks' : bytearray([54]),
	   'finish' : bytearray([55])
       }
       
       self.baseline_check_before_sleep_time = { #absolute time of baseline check .wav
       'openyoureyeslooktotheceiling' : 4000,
       'closeyoureyeslooktotheceiling' : 24000,
       'openyoureyes' : 43000,
       'clenchyourteeth' : 57000,
       'doLRLR' : 76000,
       'blink' : 89000,
       'again_clenchyourteeth' : 105000,
       'again_doLRLR' : 120000,
       'again_blink' : 133000,
       'finish' : 147000
       }
	   
       os.chdir(current_dir + '\\Audio')
       
       pygame.init()
       pygame.mixer.init()
       pygame.mixer.music.load('baseline_check_before_sleep.wav')
       pygame.mixer.music.play()
       
       baseline_check_time = self.baseline_check_before_sleep_time['openyoureyeslooktotheceiling']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events_before_sleep['look_totheceiling_eyesopen'])))
       
       baseline_check_time = self.baseline_check_before_sleep_time['closeyoureyeslooktotheceiling']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events_before_sleep['look_totheceiling_eyesclosed'])))
       
       baseline_check_time = self.baseline_check_before_sleep_time['openyoureyes']

       baseline_check_time = self.baseline_check_before_sleep_time['clenchyourteeth']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events_before_sleep['clench_teeth'])))
       
       baseline_check_time = self.baseline_check_before_sleep_time['doLRLR']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events_before_sleep['LRLR'])))
       
       baseline_check_time = self.baseline_check_before_sleep_time['blink']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events_before_sleep['eye_blinks'])))
       
       baseline_check_time = self.baseline_check_before_sleep_time['again_clenchyourteeth']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events_before_sleep['clench_teeth'])))
       
       baseline_check_time = self.baseline_check_before_sleep_time['again_doLRLR']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events_before_sleep['LRLR'])))
       
       baseline_check_time = self.baseline_check_before_sleep_time['again_blink']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events_before_sleep['eye_blinks'])))
       
       baseline_check_time = self.baseline_check_before_sleep_time['finish']
       # self.window.after(baseline_check_time, lambda:self.port2.write(str.encode(baseline_events_before_sleep['finish'])))
	   
    def motivational_speech_LDBCI(self):
	
       self.motivational_speech_events = {
       'speech' : bytearray([56])
       }
	
       os.chdir(current_dir +  '\\Audio\\Motivation Speech')
       
       pygame.init()
       # Initiating Pygame Mixer
       pygame.mixer.init()
       
       pygame.mixer.music.load('dreamBCI.wav')
       # Playing Selected Song
       pygame.mixer.music.play()
      
    def motivational_speech_dreamSpeech(self):
	
       self.motivational_speech_events = {
       'speech' : bytearray([56])
       }
	
       os.chdir(current_dir +  '\\Audio\\Motivation Speech')

       pygame.init()
       # Initiating Pygame Mixer
       pygame.mixer.init()
       
       pygame.mixer.music.load('dreamSpeech.wav')
       # Playing Selected Song
       pygame.mixer.music.play()
   
#%% ============================= Dream BCI =======================
class DreamBCI(tk.Frame): 
      
    def __init__(self, parent, controller, count=0, clenchingTime=3000, restingTime=2000): #milliseconds  
       tk.Frame.__init__(self, parent)
       
       self.config(background='black')
       self.controller = controller 
       
       self.window = parent
       # self.window.rowconfigure(2, weight=1)
       self.count = count
       self.clenchingTime = clenchingTime
       self.restingTime = restingTime
       self.textLogTime = 3000 #milliseconds
       self.initialize_user_interface(controller)
       self.real_log_data = np.empty(shape=[0])
       
       self.total_width = self.controller.total_width
       self.total_height = self.controller.total_height
       
       #===== Time Points Initialization ======
       #==== Aligning Process ====
     
       self.elapsedTimes = {
           'main_intro' : 3000,
           'relaxing' : 10000,
           'countdown' : 1000,
           'blink' : 1000
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
       #PORT_NAME = 'COM1'
       #BAUDRATE  = 115200
       #self.port = serial.Serial(PORT_NAME,baudrate=BAUDRATE)
       self.BYTEVALUES = {
 	   'get_ready' : bytearray([4]),
 	   'relax' : bytearray([5]),
       'countdown' : bytearray([6]), 
       'blink' : bytearray([7]),
 	   'finish' : bytearray([8]),
       'left'  : bytearray([1]),
       'right' : bytearray([2]),
       'rest'  : bytearray([3]),
# 	   
# 	   # free timing session events
       'welcome_session' : bytearray([11]),
       'explanation' : bytearray([12]),
       'LRLR_sequence_instruction' : bytearray([13]),
       'clench_time_explanation' : bytearray([14]),
       'free_timing_clench_teeth' : bytearray([15]),
       'short_time' : bytearray([16]),
       'regular_time' : bytearray([17]),
       'long_time' : bytearray([18]),
       'long_rest' : bytearray([19]),	   
 	   }
#   	   #====== Serial Port Connection =======
#%% ===================== User Interface ===================	   
    def initialize_user_interface(self, controller):
        
        #====== Window Initialization =======
        # self.window.title("Lucid Dream BCI GUI")
        # pad=3
        # self.window.geometry("{0}x{1}+0+0".format(self.window.winfo_screenwidth()-pad, self.window.winfo_screenheight()-pad))
        # self.window.configure(background='black') #change background color
        #====== Window Initialization =======
        
        # ===== Text Clenching ======
        self.textAction = StringVar()
        self.textAction.set("Begin")
        self.lbl = Label(self, textvariable=self.textAction, font=("Arial Bold", 60), foreground='white', background='black')
        self.lbl.place(relx=0.5, rely=0.5, anchor='center')
        self.lbl.config(font=("Arial Bold", 30))
        # ===== Text Clenching ======
        
        # ===== Text Combobox Clenching Time Interval ======
        self.textComboboxClTiInt = StringVar()
        self.textComboboxClTiInt.set("Clenching Elapsed Time (Sec) :")
        self.lbl2 = Label(self, textvariable=self.textComboboxClTiInt, font=("Arial Bold", 10), foreground='white', background='black')
        self.lbl2.place(relx=0.83, rely=0.02, anchor='center')
        # ===== Text Combobox Clenching Time Interval ======
        
        # ===== Text Combobox Resting Time Interval ======
        self.textComboboxRstTiInt = StringVar()
        self.textComboboxRstTiInt.set("Resting Elapsed Time (Sec) :")
        self.lbl3 = Label(self, textvariable=self.textComboboxRstTiInt, font=("Arial Bold", 10), foreground='white', background='black')
        self.lbl3.place(relx=0.83, rely=0.055, anchor='center')
        # ===== Text Combobox Resting Time Interval ======
        
        # ====== Text Log =========
        self.textLog = StringVar()
        self.lbl4 = Label(self, textvariable=self.textLog, font=("Arial Bold", 20), foreground='white', background='black')
        self.lbl4.place(relx=0.8, rely=0.945, anchor='center')
        # ====== Text Log =========
        
        # ====== Button ===========     
        custom_font = tkFont.Font(family='Helvetica', size=15, weight=tkFont.NORMAL)
        self.btnBegin = Button(self, text="Begin", bg="black", fg="white", font=custom_font, command=self.beginClicked)
        self.btnBegin.grid(column=1, row=0)
        self.btnBegin.config(state = DISABLED)
        self.btnPause = Button(self, text="Pause", bg="black", fg="white", font=custom_font, command=self.pauseClicked)
        self.btnPause.grid(column=2, row=0)
        self.btnPause.config(state = DISABLED)
        self.btnContinue = Button(self, text="Continue", bg="black", fg="white", font=custom_font, command=self.continueClicked)
        self.btnContinue.grid(column=3, row=0)
        self.btnContinue.config(state = DISABLED)
        self.btnExit = Button(self, text="Exit", bg="black", fg="white", font=custom_font, command=lambda: controller.exit())
        self.btnExit.grid(column=4, row=0)
        self.btnReset = Button(self, text="Reset", bg="black", fg="white", font=custom_font, command=lambda: controller.restart_dreamBCI())
        self.btnReset.grid(column=5, row=0)
        self.btnReset.config(state = DISABLED)
        self.btnMainMenu = Button(self, text="Main Menu", bg="black", fg="white", font=custom_font, \
                                  command=lambda: controller.show_frame(StartPage))
        self.btnMainMenu.grid(column=6, row=0)
        
        self.btnSequenceCreation = Button(self, text="Create a Sequence", bg="black", fg="white", \
                                          font=custom_font, command=self.settingSequence)
        self.btnSequenceCreation.place(relx=0, rely=0.07, anchor='w')
		#===== Free timing =====
        self.btnFreeTiming = Button(self, text="Free Timing Train", bg="black", fg="white", font=custom_font, \
									command=self.freetimingClicked)
        #self.btnExit.grid(column=6, row=1)
        self.btnFreeTiming.place(relx=0.9, rely=0.9, anchor='w')
        # ====== Button ===========
        
        #===== Combobox Clenching Interval ========
        self.comboClInt = ttk.Combobox(self)
        self.comboClInt['values']= (2,3,4,5) #clenching times as second
        self.comboClInt.current(1) #set the selected item
        self.comboClInt.place(relx=0.9, rely=0.01)
        self.comboClInt.bind("<<ComboboxSelected>>", self.changeClenchingInterval)
        #===== Combobox Clenching Interval ========
        
        #===== Combobox Resting Interval ========
        self.comboRestInt = ttk.Combobox(self)
        self.comboRestInt['values']= (1,2,3,4,5) #clenching times as second
        self.comboRestInt.current(1) #set the selected item
        self.comboRestInt.place(relx=0.9, rely=0.045)
        self.comboRestInt.bind("<<ComboboxSelected>>", self.changeRestingInterval)
        #===== Combobox Resting Interval ========
        
        self.btnSubmit = Button(self, text="Submit", bg="black", fg="white", font=custom_font, command=self.finish_protocol)
        self.btnSubmit.place(relx=0.5, rely=0.7, anchor='center')
        self.btnSubmit.place_forget() #hide the button
        
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
             
    # def exitClicked(self):
    #     print('Program closed!')
    #     self.window.quit()
    #     self.window.destroy()
        
    # def resetClicked(self):
              
    #     #=== Logging ====
    #     print('Process has stopped!')
    #     self.textLog.set('Process has stopped!')
    #     self.lbl4.after(1000, self.log_delete)
    #     #=== Logging ====
        
    #     # self.window.after(1000, self.restart_program, controller) #fresh restart
    #     self.window.afer(1000, lamdda)
    
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
        
        os.chdir(current_dir)
        self.sequence = pickle.load(open('Sequences/sequence', 'rb')) #82 amount is for all 3 combinations
        self.sequence = self.sequence[0:60] #decrease a bit
              
        self.btnBegin.config(state = NORMAL)
        self.btnSequenceCreation.config(state = DISABLED)
        
        #== Logging ===
        print('Sequence Loaded!')
        self.textLog.set('Sequence Loaded!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        #== Logging ===
    
    # def restart_program(self, controller):
    #     print('Program Restarting!')
    #     controller.quit()
    #     controller.destroy()
        
    #     app = tkinterApp() 
    #     app.mainloop() 
    #     # self.window.destroy()
    #     # window = Tk()
    #     # callback = GUI(parentWindow=window)
    #     # window.mainloop()
    
    def aligningTest(self):
        
        if not doTick:
            return
        
        self.startActiontime = time.time() # resting() function looks for clenching time so I had to add this one
       
        self.action_text_event_creator(textaction='Welcome!', event_text='get_ready',\
                                          event_type='normal', append=False, relx=0.5, rely=0.5)
        total_time = self.elapsedTimes['main_intro']
        
        self.window.after(total_time, self.action_text_changer, 'relax', 'Just relax yourself', 'get ready')
        total_time += self.elapsedTimes['relaxing']
        
        self.window.after(total_time, self.action_text_changer, 'countdown', 'You will begin in \n 3 seconds', 'relax')
        total_time += self.elapsedTimes['countdown']
        
        self.window.after(total_time, self.action_text_changer, 'countdown', 'You will begin in \n 2 seconds', 'countdown')
        total_time += self.elapsedTimes['countdown']
        
        self.window.after(total_time, self.action_text_changer, 'countdown', 'You will begin in \n 1 seconds', 'countdown')
        total_time += self.elapsedTimes['countdown']
        
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
        self.window.after(3000, self.attention_questionnaire)

#%% ========================= Finish Protocols ==================================

    def attention_questionnaire(self):
        self.textAction.set("")
        self.scale = Scale(self, label='Please rate your attention level from 1 to 10', from_=1, to=10, orient=tk.HORIZONTAL, length=int(self.total_width/3), showvalue=0, tickinterval=1, resolution=1, font=30, command=self.print_attention_level)
        self.scale.place(relx=0.5, rely=0.5, anchor='center')
        self.btnSubmit.place(relx=0.5, rely=0.6, anchor='center')
        
    def print_attention_level(self, v):
        print('Attention level is : %s' % v)

    def finish_protocol(self):
        
        #==== Events About Attention Level =====
        self.scale.place_forget()
        self.btnSubmit.place_forget()
        attention_level = self.scale.get()
        
        dateTime = str(datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S'))
        date = str(datetime.datetime.now().strftime('%y-%m-%d')) #name of the file
        file_object = open('Log Data/Dream BCI/Attention Levels/' + date + '.txt',"a+")
        file_object.write(dateTime + '  :: %s\n' % attention_level)
        file_object.close()
        #==== Events About Attention Level =====
        
        self.action_text_changer(textaction='The End', event_text='finish', finished_action='finished')

        self.btnBegin.config(state = NORMAL)
        self.btnPause.config(state = DISABLED)
        self.btnReset.config(state = NORMAL)
        self.btnFreeTiming.config(state = NORMAL)
        
        #=== Log-data Saving ====
        dateTime = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        
        self.real_log_data = np.append(self.real_log_data, 3) #manually add
                
        '''=========== Save Data ============'''
        default_log_time = np.array([self.elapsedTimes['main_intro'], self.elapsedTimes['relaxing'], self.elapsedTimes['countdown'], \
                                     self.elapsedTimes['countdown'], self.elapsedTimes['countdown']])
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
        pickle.dump(self.allLogData, open('Log Data/Dream BCI/' + 'allLogData_' + str(dateTime), 'wb'))
        pickle.dump(self.allInitialDateTimes, open('Log Data/Dream BCI/' + 'allInitialDateTimes_' + str(dateTime), 'wb'))
        #==== Pickle =====
        '''=========== Save Data ============'''
        
        self.textLog.set('Log Data has been saved into the directory!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        print('Log Data has been saved into the directory!')
        #=== Log-data Saving ====
        
        self.count = 0

    def freetiming_finish_protocol(self):
        
        self.freetiming_action_text_changer(textaction='The End', event_text='finish', finished_action='finished')
    
        self.btnBegin.config(state = NORMAL)
        self.btnFreeTiming.config(state = NORMAL)
        self.btnPause.config(state = DISABLED)
        self.btnReset.config(state = NORMAL)
        
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
        pickle.dump(self.allFreeTimingLogData, open('Log Data/Dream BCI/' + 'allFreeTimingLogData_' + str(dateTime), 'wb'))
        pickle.dump(self.allFreeTimingSessionDateTimes, open('Log Data/Dream BCI/' + 'allFreeTimingSessionDateTimes_' + str(dateTime), 'wb'))
        #==== Pickle =====
        '''=========== Save Data ============'''
        
        self.textLog.set('Log Data has been saved into the directory!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        print('Log Data has been saved into the directory!')
        '''============== Log-data Saving =================='''
        
        self.count = 0
    
		
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
        #self.port.write(self.BYTEVALUES[event_text]) #stimulus
        #self.controller.port.write(self.BYTEVALUES[event_text])
        #print(str(self.BYTEVALUES[event_text]))
		
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
   
#%% ========================================================================================================================================

''' ============================================================= Dream Speech ========================================================== '''  
# third window frame page2 
class DreamSpeech(tk.Frame):  
    def __init__(self, parent, controller, count=0, utteranceTime=3000, restingTime=2000, selected_wordPairs=2, totalLength=12): 
        tk.Frame.__init__(self, parent) 
        
        self.config(background='black')
        self.controller = controller 
        self.window = parent
        
        self.total_width = self.controller.total_width
        self.total_height = self.controller.total_height
        
        self.selected_wordPairs = selected_wordPairs
        self.sequence = list()
        self.count = count
        self.totalLength = totalLength
        self.utteranceTime = utteranceTime
        self.restingTime = restingTime
        self.textLogTime = 2000 #milliseconds
        self.initialize_user_interface(controller)
        self.real_log_data = np.empty(shape=[0])
        
        #==== Aligning Process ====
        self.elapsedTimes = {
           'main_intro' : 3000,
           'relaxing' : 10000,
           'countdown' : 1000,
           'blink' : 1000
           }
       #==== Aligning Process ====
        
        self.startUtteranceTime = 100 #just start speaking time to give big value for skipping first calculation!
        self.endClenchingTime = 0
        self.startRestingTime = 100
        self.endRestingTime = 0
       
        self.allInitialDateTimes = {
           'get_ready' : None,
           'relax' : None,
           'blink' : list(),
           'speak' : list(),
           'rest' : list(),
           'finish' : None,
           'all_events' : list()
           } 
        
        self.allLogData = {
           'real_elapsed_times' : None,
           'default_elapsed_times' : None,
           'chosen_sequence' : None,
           'elapsed_utterance_time' : None,
           'elapsed_resting_time' : None
           }
		   
	    #====== Serial Port Connection =======
  	    # serial port stuff
        #PORT_NAME = 'COM1'
        #BAUDRATE  = 115200
        #self.port = serial.Serial(PORT_NAME,baudrate=BAUDRATE)
        self.BYTEVALUES = {
 	    'get_ready' : bytearray([4]),
 	    'relax' : bytearray([5]),
        'countdown' : bytearray([6]),
        'blink' : bytearray([7]),
 	    'finish' : bytearray([8]),
         
 	    'speak' : bytearray([1]),
        'rest'  : bytearray([2])
 	    }
   	    #====== Serial Port Connection =======
        
#%% ==================== User Interface Initiation ====================   
    def initialize_user_interface(self, controller):
        
        # ===== Text Clenching ======
        self.textAction = StringVar()
        self.textAction.set("Begin")
        self.lbl = Label(self, textvariable=self.textAction, font=("Arial Bold", 60), foreground='white', background='black')
        self.lbl.place(relx=0.5, rely=0.5, anchor='center')
        self.lbl.config(font=("Arial Bold", 30))
        # ===== Text Clenching ======

        # ===== Text Combobox Clenching Time Interval ======
        self.textComboboxWP = StringVar()
        self.textComboboxWP.set("Word Pair Type :")
        self.lbl1 = Label(self, textvariable=self.textComboboxWP, font=("Arial Bold", 11), foreground='white', background='black')
        self.lbl1.place(relx=0.83, rely=0.02, anchor='center')
        # ===== Text Combobox Clenching Time Interval ======
        
        # ===== Text Combobox Clenching Time Interval ======
        self.textComboboxClTiInt = StringVar()
        self.textComboboxClTiInt.set("Utterance Elapsed Time (Sec) :")
        self.lbl2 = Label(self, textvariable=self.textComboboxClTiInt, font=("Arial Bold", 11), foreground='white', background='black')
        self.lbl2.place(relx=0.83, rely=0.055, anchor='center')
        # ===== Text Combobox Clenching Time Interval ======
        
        # ===== Text Combobox Resting Time Interval ======
        self.textComboboxRstTiInt = StringVar()
        self.textComboboxRstTiInt.set("Resting Elapsed Time (Sec) :")
        self.lbl3 = Label(self, textvariable=self.textComboboxRstTiInt, font=("Arial Bold", 11), foreground='white', background='black')
        self.lbl3.place(relx=0.83, rely=0.08, anchor='center')
        # ===== Text Combobox Resting Time Interval ======
        
        # ===== Text Combobox Session Length ======
        self.textComboboxSL = StringVar()
        self.textComboboxSL.set("Amount of Words :")
        self.lbl5 = Label(self, textvariable=self.textComboboxSL, font=("Arial Bold", 11), foreground='white', background='black')
        self.lbl5.place(relx=0.83, rely=0.115, anchor='center')
        # ===== Text Combobox Session Length ======
        
        # ====== Text Log =========
        self.textLog = StringVar()
        self.lbl4 = Label(self, textvariable=self.textLog, font=("Arial Bold", 15), foreground='white', background='black')
        self.lbl4.place(relx=0.8, rely=0.945, anchor='center')
        # ====== Text Log =========
        
        # ====== Button ===========     
        custom_font = tkFont.Font(family='Helvetica', size=15, weight=tkFont.NORMAL)
        self.btnBegin = Button(self, text="Begin", bg="black", fg="white", font=custom_font, command=self.beginClicked)
        self.btnBegin.grid(column=1, row=0)
        # self.btnBegin.config(state = DISABLED)
        self.btnPause = Button(self, text="Pause", bg="black", fg="white", font=custom_font, command=self.pauseClicked)
        self.btnPause.grid(column=2, row=0)
        self.btnPause.config(state = DISABLED)
        self.btnContinue = Button(self, text="Continue", bg="black", fg="white", font=custom_font, command=self.continueClicked)
        self.btnContinue.grid(column=3, row=0)
        self.btnContinue.config(state = DISABLED)
        self.btnExit = Button(self, text="Exit", bg="black", fg="white", font=custom_font, command=lambda: controller.exit())
        self.btnExit.grid(column=4, row=0)
        self.btnReset = Button(self, text="Reset", bg="black", fg="white", font=custom_font, command=lambda: controller.restart_dreamSpeech())
        self.btnReset.grid(column=5, row=0)
        self.btnReset.config(state = DISABLED)
        self.btnMainMenu = Button(self, text="Main Menu", bg="black", fg="white", font=custom_font, \
                                  command=lambda: controller.show_frame(StartPage))
        self.btnMainMenu.grid(column=6, row=0)
        
        self.btnSubmit = Button(self, text="Submit", bg="black", fg="white", font=custom_font, command=self.finish_protocol)
        self.btnSubmit.place(relx=0.5, rely=0.7, anchor='center')
        self.btnSubmit.place_forget() #hide the button
        # ====== Button ===========
        
        #====== Word Pair Selection =======
        self.comboWP = ttk.Combobox(self)
        self.comboWP['values']= ("Man, Eats, Food", "Dream, Speech", "Left, Right, Up, Down") #clenching times as second
        self.comboWP.current(2) #set the selected item
        self.comboWP.place(relx=0.9, rely=0.01)
        self.comboWP.bind("<<ComboboxSelected>>", self.change_wordPairs)
        #====== Word Pair Selection =======
        
        #===== Combobox Utterance Interval ========
        self.comboClInt = ttk.Combobox(self)
        self.comboClInt['values']= (2,3,4,5) #clenching times as second
        self.comboClInt.current(1) #set the selected item
        self.comboClInt.place(relx=0.9, rely=0.045)
        self.comboClInt.bind("<<ComboboxSelected>>", self.changeUtteranceInterval)
        #===== Combobox Utterance Interval ========
        
        #===== Combobox Resting Interval ========
        self.comboRestInt = ttk.Combobox(self)
        self.comboRestInt['values']= (1,2,3,4,5) #clenching times as second
        self.comboRestInt.current(1) #set the selected item
        self.comboRestInt.place(relx=0.9, rely=0.08)
        self.comboRestInt.bind("<<ComboboxSelected>>", self.changeRestingInterval)
        #===== Combobox Resting Interval ========
        
        #===== Combobox Session Length ========
        self.comboSessLength = ttk.Combobox(self)
        self.comboSessLength['values']= (12,24,36,48,60) #clenching times as second
        self.comboSessLength.current(0) #set the selected item
        self.comboSessLength.place(relx=0.9, rely=0.115)
        self.comboSessLength.bind("<<ComboboxSelected>>", self.change_sessionLength)
        #===== Combobox Session Length ========
        

#%% ========================== Button Actions ===========================
    def beginClicked(self):
        os.chdir(current_dir)
        
        print('Program is beginning!')
        global doTick
        doTick = True
        
        self.comboClInt.config(state = DISABLED)
        self.comboRestInt.config(state = DISABLED)
        # self.btnFreeTiming.config(state = DISABLED)
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
        
    # def resetClicked(self):
              
    #     #=== Logging ====
    #     print('Process has stopped!')
    #     self.textLog.set('Process has stopped!')
    #     self.lbl4.after(1000, self.log_delete)
    #     #=== Logging ====
        
    #     self.window.after(1000, self.restart_program) #fresh restart
    def change_wordPairs(self, event):
        self.selected_wordPairs = int(self.comboWP.current())
        
        #==== Logging =====
        print("Word Pairs has changed")
        self.textLog.set('Word Pairs has changed into ' + str(self.selected_wordPairs))
        self.lbl4.after(self.textLogTime, self.log_delete)
        #==== Logging =====
    
    def changeUtteranceInterval(self, event):
        self.utteranceTime = int(self.comboClInt.get()) * 1000
        
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
        
    def change_sessionLength(self, event):
        self.totalLength = int(self.comboSessLength.get())
        
        #==== Logging ====
        print('Total word number set as : %s' % self.comboSessLength.get())
        self.textLog.set('Total word number set as ' + str(int(self.comboSessLength.get())))
        self.lbl4.after(self.textLogTime, self.log_delete)
        #==== Logging ====
   
    #%% ======================== Text Changers ================================
    def log_delete(self):
        self.textLog.set('')
        
    def action_text_changer(self, event_text, textaction, finished_action):
        
        if(event_text == 'blink'):
            self.action_text_event_creator(textaction=textaction, event_text=event_text,\
                                           append=True, relx=0.5, rely=0.5)
        else:
            self.action_text_event_creator(textaction=textaction, event_text=event_text,\
                                           append=False, relx=0.5, rely=0.5)
        
        #=== Logging =====
        self.endActionTime = time.time()
        elapsed_action_time = self.endActionTime - self.startActiontime
        print('Elapsed ' + finished_action + ' time: %s' % elapsed_action_time)
        self.real_log_data = np.append(self.real_log_data, elapsed_action_time)
        #=== Logging =====
        
        self.startActiontime = time.time()
        self.startUtteranceTime = time.time()
    #%% ================ Actions ==========================
        
    def aligningTest(self):
        
        if not doTick:
            return
        
        self.startActiontime = time.time() # resting() function looks for clenching time so I had to add this one
       
        self.action_text_event_creator(textaction='Welcome!', event_text='get_ready',\
                                       append=False, relx=0.5, rely=0.5)
        total_time = self.elapsedTimes['main_intro']
        
        self.window.after(total_time, self.action_text_changer, 'relax', 'Just relax yourself', 'get ready')
        total_time += self.elapsedTimes['relaxing']
        
        self.window.after(total_time, self.action_text_changer, 'countdown', 'You will begin in \n 3 seconds', 'relax')
        total_time += self.elapsedTimes['countdown']
        
        self.window.after(total_time, self.action_text_changer, 'countdown', 'You will begin in \n 2 seconds', 'countdown')
        total_time += self.elapsedTimes['countdown']
        
        self.window.after(total_time, self.action_text_changer, 'countdown', 'You will begin in \n 1 seconds', 'countdown')
        total_time += self.elapsedTimes['countdown']
        
        self.window.after(total_time, lambda:self.resting()) #experiment begin
        
    def utterance(self):
        
        if not doTick:
            return
        
        #======= Resting Time Calculation =======
        self.endRestingTime = time.time()
        elapsed_restingTime = self.endRestingTime - self.startRestingTime
        self.real_log_data = np.append(self.real_log_data, elapsed_restingTime)
        if(elapsed_restingTime > 0):
            print("Elapsed Resting Time = %s" % elapsed_restingTime)
        #======= Resting Time Calculation =======
      
        # if(actionType == '0'):
       
        #    self.action_text_event_creator(textaction='L', event_text='left',\
        #                                   event_type='normal', append=True, relx=0.47, rely=0.5)
           
        # else:
           
        #    self.action_text_event_creator(textaction='R', event_text='right',\
        #                                   event_type='normal', append=True, relx=0.53, rely=0.5)
        if(self.selected_wordPairs == 0):
            if(self.count % 3 == 0):
                 self.action_text_event_creator(textaction='"Man"', event_text='speak',\
                                                append=True, relx=0.5, rely=0.5)
                 self.sequence.append('Man')
            elif(self.count % 3 == 1):
                 self.action_text_event_creator(textaction='"Eats"', event_text='speak',\
                                                append=True, relx=0.5, rely=0.5)
                 self.sequence.append('Eats')
            elif(self.count % 3 == 2):
                 self.action_text_event_creator(textaction='"Food"', event_text='speak',\
                                                append=True, relx=0.5, rely=0.5)
                 self.sequence.append('Food')
        elif(self.selected_wordPairs == 1):
            if(self.count % 2 == 0):
                 self.action_text_event_creator(textaction='"Dream"', event_text='speak',\
                                                append=True, relx=0.5, rely=0.5)
                 self.sequence.append('Dream')
            elif(self.count % 2 == 1):
                 self.action_text_event_creator(textaction='"Speech"', event_text='speak',\
                                                append=True, relx=0.5, rely=0.5)
                 self.sequence.append('Speech')   
        elif(self.selected_wordPairs == 2):
            if(self.count % 4 == 0):
                 self.action_text_event_creator(textaction='"Left"', event_text='speak',\
                                                append=True, relx=0.5, rely=0.5)
                 self.sequence.append('Left')
            elif(self.count % 4 == 1):
                 self.action_text_event_creator(textaction='"Right"', event_text='speak',\
                                                append=True, relx=0.5, rely=0.5)
                 self.sequence.append('Right')
            elif(self.count % 4 == 2):
                 self.action_text_event_creator(textaction='"Up"', event_text='speak',\
                                                append=True, relx=0.5, rely=0.5)
                 self.sequence.append('Up')
            elif(self.count % 4 == 3):
                 self.action_text_event_creator(textaction='"Down"', event_text='speak',\
                                                append=True, relx=0.5, rely=0.5)         
                 self.sequence.append('Down')    
            
        self.window.update() #window update ne hikmetse ise yaradi!!
        self.count += 1 #next
        
        self.startUtteranceTime = time.time()
        self.window.after(self.utteranceTime, self.resting) #do not call method with parameters inside like x(n1,n2)
                                                                                         #this method at first wait than works 
                                                                                         
    def resting(self):
        
        if not doTick:
            return
        
        self.lbl.config(font=("Arial Bold", 60))
        #======= Clenching Time Calculation =====
        self.endUtteranceTime = time.time()
        elapsed_utteranceTime = self.endUtteranceTime - self.startUtteranceTime
        self.real_log_data = np.append(self.real_log_data, elapsed_utteranceTime)
        print("Elapsed Utterance Time = %s" % elapsed_utteranceTime)
        #======= Clenching Time Calculation =====
        
        self.startRestingTime = time.time()
        
        #====== If End ========
        if(self.count == self.totalLength):
            self.last_blinks_protocol()
            return
        #====== If End ========
        
        #===== Resting =====
        self.action_text_event_creator(textaction='X', event_text='rest',\
                                       append=True)
        self.window.update() #window update ne hikmetse ise yaradi!!
        
        
        self.window.after(self.restingTime, self.utterance)
        #===== Resting =====
        
    def last_blinks_protocol(self):
       
        self.action_text_event_creator(textaction='Please blink as much as possible', event_text='blink',\
                                       append=True)
        
        self.startActiontime = time.time()
        self.window.after(3000, self.attention_questionnaire) 

#%% ============================= Special Functions ======================
    def action_text_event_creator(self, textaction, event_text, append=False, relx=0.5, rely=0.5):
        self.textAction.set(textaction)
        self.lbl.place(relx=relx, rely=rely, anchor='center')
        #self.port.write(self.BYTEVALUES[event_text]) #stimulus
        #self.controller.port.write(self.BYTEVALUES[event_text])
        #print(str(self.BYTEVALUES[event_text]))
		
        current_time = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S.%f')[:-3]

        '''==== Current time Adding ====='''
        if(append==True):
            self.allInitialDateTimes[event_text].append(current_time)
        else:
            self.allInitialDateTimes[event_text] = current_time
            
        self.allInitialDateTimes['all_events'].append(current_time)
        '''==== Current time Adding ====='''
        
#%% ========================= Finish Protocols ==================================

    def attention_questionnaire(self):
        self.textAction.set("")
        self.scale = Scale(self, label='Please rate your attention level from 1 to 10', from_=1, to=10, orient=tk.HORIZONTAL, length=int(self.total_width/3), showvalue=0, tickinterval=1, resolution=1, font=30, command=self.print_attention_level)
        self.scale.place(relx=0.5, rely=0.5, anchor='center')
        self.btnSubmit.place(relx=0.5, rely=0.6, anchor='center')
        
    def print_attention_level(self, v):
        print('Attention level is : %s' % v)

    def finish_protocol(self):
        
        #==== Events About Attention Level =====
        self.scale.place_forget()
        self.btnSubmit.place_forget()
        attention_level = self.scale.get()
        
        dateTime = str(datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S'))
        date = str(datetime.datetime.now().strftime('%y-%m-%d')) #name of the file
        file_object = open('Log Data/Dream Speech/Attention Levels/' + date + '.txt',"a+")
        file_object.write(dateTime + '  :: %s\n' % attention_level)
        file_object.close()
        #==== Events About Attention Level =====
        
        self.action_text_changer(textaction='The End', event_text='finish', finished_action='finished')

        self.btnBegin.config(state = NORMAL)
        self.btnPause.config(state = DISABLED)
        self.btnReset.config(state = NORMAL)
        # self.btnFreeTiming.config(state = NORMAL)
        
        #=== Log-data Saving ====
        dateTime = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        
        self.real_log_data = np.append(self.real_log_data, 3) #manually add
                
        '''=========== Save Data ============'''
        default_log_time = np.array([self.elapsedTimes['main_intro'], self.elapsedTimes['relaxing'], self.elapsedTimes['countdown'], \
                                     self.elapsedTimes['countdown'], self.elapsedTimes['countdown']])
        default_log_time = default_log_time / 1000
            
        for i in range(len(self.sequence)):
            default_log_time = np.append(default_log_time, self.restingTime / 1000)
            default_log_time = np.append(default_log_time, self.utteranceTime / 1000)
        default_log_time = np.append(default_log_time, 3) #blinks           
        
        self.allLogData['real_elapsed_times'] = self.real_log_data
        self.allLogData['default_elapsed_times'] = default_log_time
        self.allLogData['chosen_sequence'] = self.sequence
        self.allLogData['elapsed_clenching_time'] = self.utteranceTime / 1000
        self.allLogData['elapsed_resting_time'] = self.restingTime / 1000
       
        #==== Pickle =====
        pickle.dump(self.allLogData, open('Log Data/Dream Speech/' + 'allLogData_' + str(self.selected_wordPairs) + '_' + str(dateTime), 'wb'))
        pickle.dump(self.allInitialDateTimes, open('Log Data/Dream Speech/' + 'allInitialDateTimes_' +  str(self.selected_wordPairs) + \
                                              '_' + str(dateTime), 'wb'))
        #==== Pickle =====
        '''=========== Save Data ============'''
        
        self.textLog.set('Log Data has been saved into the directory!')
        self.lbl4.after(self.textLogTime, self.log_delete)
        print('Log Data has been saved into the directory!')
        #=== Log-data Saving ====
        
        self.sequence = list() #empty the sequence list
        self.count = 0 

#%% ======================= Lucidity Induction ====================
class LucidityInduction(tk.Frame):
    
   def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 
          
        self.config(background='black')
        self.controller = controller
        
        self.btnAudioVisual = tk.Button(self, text ="Audio & Visual", command = lambda : self.audio_visual(), \
                                bg="black", fg="white", width = 50, height = 5, font=20) 
        self.btnAudioVisual.grid(row = 0, column = 0, padx = 10, pady = 10) 
        
        #self.btnBinauralBeats = tk.Button(self, text ="Binaural Beats", command = lambda : controller.show_frame(DreamBCI), \
        #                        bg="black", fg="white", width = 50, height = 50, font=20) 
        #self.btnBinauralBeats.grid(row = 0, column = 1, padx = 0, pady = 10) 
        
        #self.btnASMR = tk.Button(self, text ="ASMR", command = lambda : controller.show_frame(DreamBCI), \
        #                        bg="black", fg="white", width = 50, height = 50, font=20) 
        #self.btnASMR.grid(row = 0, column = 2, padx = 0, pady = 10) 
       
        #self.btnExit = tk.Button(self, text ="Exit", command = lambda : controller.exit(), \
        #                    bg="black", fg="white", width = 250, height = 5, font=20) 
        #self.btnExit.grid(row = 1, column = 0, padx = 0, pady = 10)    
        
        self.btnMainMenu = tk.Button(self, text="Main Menu", fg="white", bg="black", width = 150, \
                                       height = 5, font=20, command=lambda: controller.show_frame(StartPage))
        self.btnMainMenu.grid(row=2, column=0, padx = 0, pady = 10)
		
		#=== Port connection ====
        PORT_NAME = 'COM2'
        BAUDRATE  = 115200
        #self.port2 = serial.Serial(PORT_NAME,baudrate=BAUDRATE)
		#=== Port connection ====
		
		#==== Default Settings ======
        self.time = 3000 #ms
        self.frequency = 3 #perseq
    
   def audio_visual(self):
        print("Nothing Happens because you are not in the EEG-lab-1!")
        #os.chdir('D:/Users/cagdem/Lucid-Dream-BCI/Visual_Audio_Stimulation')
        #self.port2.write(str.encode('$rst%'))
        #self.port2.write(str.encode('$1 1 1%'))
        #time.sleep(0.2)
        #self.port2.write(str.encode('$1000 3%'))
        #self.port2.write(str.encode('$go%'))
        #self.port2.write(bytearray([4]))
        #self.controller.port.write(bytearray([99]))
		
        #winsound.PlaySound('Tone01_single.wav', winsound.SND_ASYNC)
        #time.sleep(1.25)
   
   def change_time(self, time):
       self.time = time	 
       str_encode = str(self.time + ' ' + str(self.frequency) + '%')
       #self.port2.write(str.encode(str_encode))	
	   
   def change_frequency(self, frequency):
	   self.frequency = frequency	 
	   str_encode = str(self.time + ' ' + str(self.frequency) + '%')	
	   #self.port2.write(str.encode(str_encode))
	
#%% ======================= Music and Sleep ====================
class MusicandSleep(tk.Frame):
    
   def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 
        
        print("Music and sleep has begun")
        
        self.config(background='black')
        self.controller = controller
        
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()
        
        #=== Port connection ====
        PORT_NAME = 'COM2'
        BAUDRATE  = 115200
        #self.port2 = serial.Serial(PORT_NAME,baudrate=BAUDRATE)
		#=== Port connection ====
        
        self.play_sound_events = {
	   'play' : bytearray([50]),
	   'pause' : bytearray([51]),
       'stop' : bytearray([52])
       }
    
        #======================== Music Player Frame ==================================
    
        # Creating the Track Frames for Song label & status label
        trackframe = LabelFrame(self, text="Song Track",font=("times new roman",15,"bold"),bg="Navyblue",fg="white",bd=5,relief=GROOVE)
        trackframe.place(x=50,y=50,width=600,height=100)
        # Inserting Song Track Label
        songtrack = Label(trackframe,textvariable=self.track,width=20,font=("times new roman",24,"bold"),bg="Orange",fg="gold").grid(row=0,column=0,padx=10,pady=5)
        # Inserting Status Label
        trackstatus = Label(trackframe,textvariable=self.status,font=("times new roman",24,"bold"),bg="orange",fg="gold").grid(row=0,column=1,padx=10,pady=5)
    
        # Creating Button Frame
        buttonframe = LabelFrame(self, text="Control Panel",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        buttonframe.place(x=50,y=150,width=600,height=100)
        # Inserting Play Button
        playbtn = Button(buttonframe,text="Start",command=self.startsong,width=10,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=0,padx=10,pady=5)
        # Inserting Pause Button
        playbtn = Button(buttonframe,text="Pause",command=self.pausesong,width=8,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=1,padx=10,pady=5)
        # Inserting Unpause Button
        playbtn = Button(buttonframe,text="Play",command=self.playsong,width=10,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=2,padx=10,pady=5)
        # Inserting Stop Button
        playbtn = Button(buttonframe,text="Stop",command=self.stopsong,width=10,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=3,padx=10,pady=5)
    
        # Creating Playlist Frame
        songsframe = LabelFrame(self, text="Song Playlist",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        songsframe.place(x=650,y=50,width=400,height=200)
        # Inserting scrollbar
        scrol_y = Scrollbar(songsframe,orient=VERTICAL)
        # Inserting Playlist listbox
        self.playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="gold",selectmode=SINGLE,font=("times new roman",12,"bold"),bg="silver",fg="navyblue",bd=5,relief=GROOVE)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        # Changing Directory for fetching Songs
        os.chdir(current_dir +  '\\Audio\\Soothing Music')
        # Fetching Songs
        songtracks = os.listdir()
        # Inserting Songs into Playlist
        for track in songtracks:
          self.playlist.insert(END,track) 
              
        #======================== Music Player Frame ==================================  
        
        #================ Exec File ==================
        
        #================ Exec File ==================
        
        #======================== Other Functions ===================================
        self.btnMainMenu = tk.Button(self, text="Main Menu", fg="white", bg="black", width = 150, \
                                        height = 5, font=20, command=lambda: controller.show_frame(StartPage))
        # self.btnMainMenu.grid(row=2, column=0, padx = 0, pady = 10)
        self.btnMainMenu.place(x=50,y=300,width=600,height=100)
        #======================== Other Functions ===================================
    
   def startsong(self):
        os.chdir(current_dir +  '\\Audio\\Soothing Music')
       
        # Displaying Selected Song title
        self.track.set(self.playlist.get(ACTIVE))
        # Displaying Status
        self.status.set("-Playing")
        # Loading Selected Song
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        # Playing Selected Song
        pygame.mixer.music.play()
        
        #self.port2.write(str.encode(play_sound_events['play']))
        
   def stopsong(self):
        os.chdir(current_dir +  '\\Audio\\Soothing Music')
       
        # Displaying Status
        self.status.set("-Stopped")
        # Stopped Song
        pygame.mixer.music.stop()
        
        #self.port2.write(str.encode(play_sound_events['stop']))
    
   def pausesong(self):
        os.chdir(current_dir +  '\\Audio\\Soothing Music')
       
        # Displaying Status
        self.status.set("-Paused")
        # Paused Song
        pygame.mixer.music.pause()
        
        #self.port2.write(str.encode(play_sound_events['pause']))
        
   def playsong(self):
        os.chdir(current_dir +  '\\Audio\\Soothing Music')
       
        # It will Display the  Status
        self.status.set("-Playing")
        # Playing back Song
        pygame.mixer.music.unpause()
        
# Driver Code 
app = tkinterApp() 
app.mainloop() 
