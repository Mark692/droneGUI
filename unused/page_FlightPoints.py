'''
Created on Jan 20, 2019

@author: mark
'''

from tkinter import ttk  # Sort of CSS for TKinter
import tkinter as tk  # Base graphics

try:
    from page_LogGroups import logGroups
except ImportError:
    None

    
class flightPoints(tk.Frame):
    '''
    tk.Frame - Frame used to host the log groups
    '''
    
    lg_Text = "Your flight destinations"
    LARGE_FONT0 = ("Verdana", 14)
    txt_logGroups = "Set your log groups"
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self,
                         text=self.lg_Text,
                         font=self.LARGE_FONT0)
        label.pack(pady=10, padx=10)
        
        goTo_LogGroups = ttk.Button(self,
                           text=self.txt_logGroups,
                           command=lambda: controller.show_frame(logGroups))
                            # command - used to pass functions
                            # lambda - creates a quick throwaway function
        goTo_LogGroups.pack()
        
    
    