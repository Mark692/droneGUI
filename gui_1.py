'''
Created on Oct 24, 2018

@author: mark
'''

import tkinter as tk  # Base graphics
from tkinter import ttk #CSS for TkInter
#import matplotlib.animation as mat_animation
import pages as page


liveUpdateInterval = 100  # Live graph will update each 100ms


class MainCore(tk.Tk):

    def __init__(self, *args, **kwargs):
        '''
        *args: random number of arguments
        **kwargs: dictionary to use
        '''
        
        #On online tutorials you may see a "root" object acting as the tk.Tk below
        #Just adapt the material online to tk.Tk
        #Because yes.
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'BitCraze Crazyflie Quadcopter Drones GUI')  # sets the window name
        
        wholeWindowContainer = tk.Frame(self)
        wholeWindowContainer.pack(side="top", fill="both", expand=True)
        wholeWindowContainer.grid_rowconfigure(0, weight=1)
        wholeWindowContainer.grid_columnconfigure(0, weight=1)
        
            
        #MENU DEFINITION -------------------------------------------\\
            
        #Source = https://youtu.be/7VsyZLl5DRg?list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk
        menuBar_container = tk.Menu(wholeWindowContainer)
        
        #Tab 1 - Connection
        connection_tab = tk.Menu(menuBar_container, tearoff = 0)
        connection_tab.add_command(label = "Start log and flight",
                                   command = lambda:self.showPage(wholeWindowContainer, page.droneScan))
        
        connection_tab.add_separator()
        
        connection_tab.add_command(label = "Exit",
                                   command = quit)
        menuBar_container.add_cascade(label = "Connection", 
                                      menu = connection_tab)
        self.addVerticalMenuSeparator(menuBar_container)
        

        #Tab 2 - Log Groups
        connection_tab = tk.Menu(menuBar_container, tearoff = 0)
        connection_tab.add_command(label = "Edit log groups",
                                   command = lambda:self.showPage(wholeWindowContainer, page.logGroups))
        #=======================================================================
        # connection_tab.add_separator()
        # connection_tab.add_command(label = "Info about logging"
        #                            #, command = quit
        #                            )
        #=======================================================================
        menuBar_container.add_cascade(label = "Log Groups", 
                                      menu = connection_tab)
        self.addVerticalMenuSeparator(menuBar_container)
        
        
        #Tab 3 - Flight Points
        connection_tab = tk.Menu(menuBar_container, tearoff = 0)
        connection_tab.add_command(label = "Set flight points",
                                   command = lambda:self.showPage(wholeWindowContainer, page.flightPoints))
        #=======================================================================
        # connection_tab.add_separator()
        # connection_tab.add_command(label = "Info about flight"
        #                            #, command = quit
        #                            )
        #=======================================================================
        menuBar_container.add_cascade(label = "Flight Points", 
                                      menu = connection_tab)



        #Finally add the menu tabs (created above) to the GUI
        tk.Tk.config(self, menu = menuBar_container)
        
        
        
        #At the end of __init__ show the welcome page
        
        #=======================================================================
        # self.dictionary = {}  # Dictionary definition
        # myPagesList = [page.droneScan,
        #                page.welcomeConnected,
        #                page.flightPoints, 
        #                page.logGroups, 
        #                page.WelcomePage] 
        # for newPageToShow in (myPagesList):
        #          
        #     frame = newPageToShow(wholeWindowContainer, self)
        #     frame.grid(row=0, column=0, sticky="nsew")  # The frame will strech to the whole window
        #     self.dictionary[newPageToShow] = frame
        #=======================================================================
        #self.show_frame(newPageToShow)
        
        self.showPage(wholeWindowContainer, page.WelcomePage)
        
        
    
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))    
        
    
        
    def popupmsg(self, pop_text):
        '''
        Add a Popup message to show
        Source: https://youtu.be/TQJRM8hIbXA?list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk
        '''
        msg = tk.Tk()
        msg.wm_title("Please consider:")
        label = ttk.Label(msg, text = pop_text)
        label.pack(side = 'top', fill = 'x', pady = 10)
        btn = ttk.Button(msg, 
                         text = "Confirm", 
                         command = msg.destroy)
        btn.pack()
        msg.mainloop()    
        
        
    def addVerticalMenuSeparator(self, menuContainter):
        '''
        Add 3 vertical dots (\u22EE) in the menu
        '''
        menuContainter.add_command(label="\u22EE",
                                   activebackground=menuContainter.cget("background"))
        
        
    def showPage(self, wholeWindowContainer, pageToShow):
        frame = pageToShow(wholeWindowContainer, self)
        frame.grid(row=0, column=0, sticky="nsew")  # The frame will strech to the whole window
        frame.tkraise()
            
        
        
    def show_frame(self, frameController):
 
        frame = self.dictionary[frameController]
        frame.tkraise()  # Makes the frame visible


#animated = mat_animation.FuncAnimation(anime.myFigure, anime.animate, interval=liveUpdateInterval)
# plt.show()  #Enables to show the anime.myFigure which is useless


my_gui = MainCore()
my_gui.mainloop()
