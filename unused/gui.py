'''
Created on Oct 24, 2018

@author: mark
'''

import tkinter as tk  # Base graphics
from tkinter import ttk #CSS for TkInter
import pages as page

     

class MainCore(tk.Frame):

    def __init__(self, master = None):
        '''
        master = root = tk.Tk()
        Source: https://docs.python.org/3/library/tkinter.html#tkinter-modules
        '''
        super().__init__(master)
        wholeWindowContainer = tk.Frame(self)
        wholeWindowContainer.master = master
        wholeWindowContainer.pack(side="top", fill="both", expand=True)
        wholeWindowContainer.grid_rowconfigure(0, weight=1)
        wholeWindowContainer.grid_columnconfigure(0, weight=1)
        
        self.createMenu(root)
        #self.showHome(root)
        self.showingPage = page.WelcomePage(root, self).tkraise()
            
    def createMenu(self, root):
            
        #MENU DEFINITION -------------------------------------------\\
            
        #Source = https://youtu.be/7VsyZLl5DRg?list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk
        menuBar_container = tk.Menu(root)
        
        #Tab 1 - Connection
        connection_tab = tk.Menu(menuBar_container, tearoff = 0)
        connection_tab.add_command(label = "Connect to...",
                                   #command = lambda:self.showPage(root, page.droneScan))
                                   command = lambda:self.showDroneScanPage(root))
        connection_tab.add_separator()
        connection_tab.add_command(label = "Exit",
                                   command = quit)
        menuBar_container.add_cascade(label = "Connection", 
                                      menu = connection_tab)
        self.addVerticalMenuSeparator(menuBar_container)
        
    
        #Tab 2 - Log Groups
        connection_tab = tk.Menu(menuBar_container, tearoff = 0)
        connection_tab.add_command(label = "Edit log groups",
                                   command = lambda:self.showPage(root, page.logGroups))
        connection_tab.add_separator()
        connection_tab.add_command(label = "Info about logging"
                                   #, command = quit
                                   )
        menuBar_container.add_cascade(label = "Log Groups", 
                                      menu = connection_tab)
        self.addVerticalMenuSeparator(menuBar_container)
        
        
        #Tab 3 - Flight Points
        connection_tab = tk.Menu(menuBar_container, tearoff = 0)
        connection_tab.add_command(label = "Set flight points",
                                   command = lambda:self.showPage(root, page.flightPoints))
        connection_tab.add_separator()
        connection_tab.add_command(label = "Info about flight"
                                   #, command = quit
                                   )
        menuBar_container.add_cascade(label = "Flight Points", 
                                      menu = connection_tab)
    
    
    
        #Finally add the menu tabs (created above) to the GUI
        root.config(menu = menuBar_container)
        
    
        
    def showDroneScanPage(self, root):
        self.showingPage = page.droneScan(root, self).tkraise()
        
        
    def showHome(self, root): 
        #At the end of __init__ show the welcome page
        
        self.dictionary = {}  # Dictionary definition
        myPagesList = [page.droneScan,
                       page.welcomeConnected,
                       page.flightPoints, 
                       page.logGroups, 
                       page.WelcomePage] 
        for newPageToShow in (myPagesList):
                
            frame = newPageToShow(root, self)
            frame.grid(row = 0, column = 0, sticky = "NSEW")  # The frame will strech to the whole window
            self.dictionary[newPageToShow] = frame
        #self.show_frame(newPageToShow)
        self.showPage(root, newPageToShow)
            
        
        
    def show_frame(self, frameController):
        frame = self.dictionary[frameController]
        frame.tkraise()  # Makes the frame visible
        
        
        
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
        
        
    def showPage(self, root, pageToShow):
        frame = pageToShow(root, self)
        frame.grid(row=0, column=0, sticky="nsew")  # The frame will strech to the whole window
        frame.tkraise()



root = tk.Tk()
root.wm_title('BitCraze Crazyflie Quadcopter Drones GUI')  # sets the window name
my_gui = MainCore(master = root)
my_gui.mainloop()
