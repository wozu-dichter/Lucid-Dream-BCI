In order to use guiv1.1.py you need to install relevant packages inside command prompt (cmd) for windows operating systems and
terminal for linux operating systems.

To run the program:
1- https://www.anaconda.com/distribution/ (for both windows, linux, mac) Download Python3.7 distribution software
2- Open conda prompt and type these: 
   * conda install tkinter
   * conda install numpy
   * conda install time
1- go to the folder that guiv1.1.py inside and type this:
   * python guiv1.1.py

Usage:
- There are 4 buttons:
  * Begin : Just initialization and starting button
  * Pause : Pausing button during process. You should enter Begin button during Pause state to continue
  * Exit : Exit the program
  * Reset : Reset all states to initial state
- There are 2 combobox on the top-right:
  * Clenching elapsed time (2,3,4,5)
  * Resting elapsed time (1,2,3,4)
  * You can change elapsed times during Pause state or initial state and new elapsed times will automatically activate just 
    after change. 