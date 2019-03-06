'''
Created on Jan 20, 2019

@author: mark
'''

from tkinter import ttk  # Sort of CSS for TKinter
import tkinter as tk  # Base graphics

try:
    from page_FlightPoints import flightPoints
except ImportError:
    None


    
class logGroups(tk.Frame):
    '''
    tk.Frame - Frame used to host the log groups
    '''
    
    lg_Text = "Your logging groups"
    LARGE_FONT0 = ("Verdana", 12)
    txt_FlightPoints = "Set Flight"
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self,
                         text=self.lg_Text,
                         font=self.LARGE_FONT0)
        label.pack(pady=10, padx=10)
        
        goTo_FlightPoints = ttk.Button(self,
                           text=self.txt_FlightPoints,
                           command=lambda: controller.show_frame(flightPoints))
                            # command - used to pass functions
                            # lambda - creates a quick throwaway function
        goTo_FlightPoints.pack()
        
    
    