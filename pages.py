'''
Created on Oct 24, 2018
This module is dedicated to set up pages to display

@author: mark
'''
# Base graphics
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure
from tkinter import ttk  # Sort of CSS for TKinter
import tkinter as tk  # Base graphics
from tkinter.tix import *
from Connection import findMyDrone
from tkinter import StringVar, Radiobutton
import time
#import threading
from BaseLog import LoggingExample as log
from variablesToLog import cluster
import variablesToLog
import watchtower
#from watchtower import flightTypes

# Matplotlib graphs

LARGE_FONT0 = ("Verdana", 12)
LARGE_FONT1 = ("Arial", 8)
LARGE_FONT2 = ("Times New Roman", 14)
LARGE_FONTg = ("Verdana", 22)

welcomePageLabel = "Hi!"
welcomePageButton = "Go back home"

win_width = 1300
win_height = 500



elapsedTime = 0
connection = findMyDrone()
connection.gui_scanForDrones()
drones = connection.get_dronesList()
selectedDrone = ""

logVars = variablesToLog.dictionary
logGroups_EntryButtons = []
logGroups_Values = []
toLog = []

flightTypes = watchtower.flightTypes
flightVars = watchtower.flightVars
flightPoints_EntryButtons = []
flightPoints_Values = []


    
class WelcomePage(tk.Frame):
    '''
    tk.Frame - Frame used to host the WelcomePage
    '''
    
    LARGE_FONT2 = ("Times New Roman", 12)
    txt_logGroups = "Log Groups"
    txt_flightPoints = "Flight Points"
    
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root, 
                                width=win_width, 
                                height=win_height)
        label = ttk.Label(self,
                         text=welcomePageLabel,
                         font=LARGE_FONT0)
        label.grid(row=0, column=0, sticky="WE")
        
        ttk.Label(self,
                         text="",
                         font=LARGE_FONT2).grid(row=1, column=0, sticky="nsew")
        
        buttonSCAN = ttk.Button(self,
                           text="Scan for drones!",
                           #command=lambda: self.findDrones(root, controller))
                           command=lambda: controller.showPage(root, droneScan))
        
        buttonSCAN.grid(row=2, column=0, sticky="WE")
        
        ttk.Label(self,
                         text="",
                         font=LARGE_FONT2).grid(row=3, column=0, sticky="nsew")
        
        label = ttk.Label(self,
                         text="With me you can select a drone to connect to\nchoose the variables to log\nand set flight commands!",
                         font=LARGE_FONT2)
        label.grid(row=4, column=0, sticky="nsew")
    
        
class droneScan(tk.Frame):
    '''
    tk.Frame - Frame used to host the drones available at the moment
    ToDo: This class will block any execution until a drone is correctly found (not necessarly connected)
            You may want to do some multi-threading in order to make things work smoother 
            Patch 1 - I've put a timeout so to hide the problem
    '''
    
    lg_Text = "Choose a drone to connect to"
    LARGE_FONT0 = ("Verdana", 18)
    
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root, 
                                width=win_width, 
                                height=win_height)
        label = ttk.Label(self,
                         text=self.lg_Text,
                         font=self.LARGE_FONT0)
        label.grid(row=0, column=0)
        
        
        #Scan the radio channel looking for drones
        #connection = findMyDrone()
        global drones
        drones = connection.get_dronesList()
        
        lookingForDrones_text = "This is what I've found so far"
        label = ttk.Label(self,
                     text=lookingForDrones_text,
                     font=self.LARGE_FONT0)
        label.grid(row=0, column=0, sticky="nsew")
       
        global elapsedTime
        elapsedTime = 0
        timeout = 3 #seconds
        while len(drones) == 0 and elapsedTime < timeout:
            time.sleep(1)
            elapsedTime += 1
            connection.gui_scanForDrones()
            drones = connection.get_dronesList()
        
        
        if len(drones) == 0 and elapsedTime >= timeout:

            ttk.Label(self, text="").grid()
            
            immafailure = "Nothing, I'm truly sorry :("
            label = ttk.Label(self,
                         text=immafailure,
                         font=("Verdana", 12))
            label.grid()
            
            ttk.Label(self, text="").grid()
        
            reScan = ttk.Button(self,
                               text="Scan again on the radio channel!",
                               command=lambda: controller.showPage(root, droneScan))
            reScan.grid()
            
            
        if len(drones) != 0:
            self.selected = tk.StringVar()
            self.selected.set(drones[0][0]) #Set as "selected" the first drone found
            for d in drones:
                ttk.Radiobutton(self, 
                               text = d[0],
                               variable = self.selected,
                               value = d[0]).grid()
                
            btn_ConnectToDrone = ttk.Button(self,
                               text="Connect!",
                               command=lambda: self.connectAction(root, controller))
            btn_ConnectToDrone.grid()
        
        
    def connectAction(self, root, controller):
        '''
        Based on the selected drone, chose the following action.
        It may restart the scan if the drone has lost connection,
        It may proceed to the real welcome page if the drone is correctly connected
        '''
        #https://likegeeks.com/python-gui-examples-tkinter-tutorial/
        global selectedDrone
        selectedDrone = str(self.selected.get()) #https://www.tutorialspoint.com/python/tk_radiobutton.htm
        
        if selectedDrone == "" or selectedDrone == None:
            controller.showPage(root, droneScan)
        else:
            controller.showPage(root, welcomeConnected)
            
    
class welcomeConnected(tk.Frame):
    '''
    tk.Frame - Frame used to host the initial page after connecting to a drone
    '''
    
    global selectedDrone 
    #lg_Text = "You are connected to " + selectedDrone
    LARGE_FONT0 = ("Verdana", 14)
    txt_logGroups = "START LOG AND FLIGHT!"
    
    def __init__(self, root, controller):
        
        if selectedDrone == "" or selectedDrone == None:
            controller.showPage(root, droneScan)
            
        else:
            tk.Frame.__init__(self, root, 
                                width=win_width, 
                                height=win_height)
            label = ttk.Label(self,
                             font=self.LARGE_FONT0)
            label.configure(text = "You are connected to " + selectedDrone)
            label.grid(row=0, column=0, sticky="nsew")
    
            
            button1 = ttk.Button(self,
                               text=self.txt_logGroups,
                               command = lambda:self.start_LogFlight(root, controller))
            button1.grid()
        
        
    def start_LogFlight(self, root, controller):
        global selectedDrone
        
        if selectedDrone == "" or selectedDrone == None:
            controller.showPage(root, droneScan)
            
        else:
            self.startLogging()
            self.startFlying()
            controller.showPage(root, droneScan)
            
            

    def startLogging(self):
        saveLogGroupState(self)
        global logGroups_Values
        global toLog
        global selectedDrone
        
            
        if len(logGroups_Values) != 0:
            
            supportList = []
            for group in logGroups_Values:
                for i in range(6):
                    if group[i+1] != "None":
                        supportList.append(group[i+1])
                        
                if len(supportList) != 0:
                    groupName = group[0]
                    groupTime = int(group[7])
                    c = cluster(groupName, groupTime, supportList)
                    toLog.append(c.getLogConfiguration())
                    
        if len(toLog) != 0:
            delay = self.getFlightTimeLength()
            if delay == float(0):
                log(selectedDrone, toLog)
            else:
                delay += 10 #Add some extra delay at the end
                log(selectedDrone, toLog, delay)
    
    
    def getFlightTimeLength(self):
        global flightPoints_Values
        global flightTypes
        
        delay = 0
        for f in flightPoints_Values:
            if f[0] != flightTypes[0]:
                delay += float(int(f[5]) * float(f[6]))
                
        return delay/1000
        
        
    def startFlying(self):
        saveFlightState(self)
        global flightPoints_Values
        global selectedDrone
        
        watchtower.toInfinity(selectedDrone, flightPoints_Values)
            
        
    
    
class flightPoints(tk.Frame):
    '''
    tk.Frame - Frame used to host the log groups
    '''
    
    lg_Text = "Your flight destinations"
    LARGE_FONT0 = ("Verdana", 14)
    txt_logGroups = "Set your log groups"
    
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root, 
                                width=win_width, 
                                height=win_height)
        label = ttk.Label(self,
                         text=self.lg_Text,
                         font=self.LARGE_FONT0,
                         justify="right")
        label.grid(row=0, column=0, columnspan = 3, sticky="EW")
        
        
        saveLogGroupState(self)
        
        
        #Add the right-horizontal scrollbar
        #Source: https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
        self.canvas = tk.Canvas(self, 
                                width=win_width, 
                                height=win_height,
                                borderwidth=0)
        self.frame = tk.Frame(self.canvas,
                                width=win_width, 
                                height=win_height)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.grid(row = 1, rowspan = 10, sticky="NSE")
        self.canvas.grid(row = 1, rowspan = 10, sticky="NSWE")
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)   
        
        
        #Separator
        horizontalSeparator = ttk.Label(self,
                              text = "")
        horizontalSeparator.grid(column = 0, columnspan = 10)
        
        
        global flightPoints_Values
        totalFlights = len(flightPoints_Values)
        
        if totalFlights != 0:
            for f in range(totalFlights):
                self.addFlightPoint(
                                   flightID = f,
                                   root = root, controller = controller,
                                   flightType = flightPoints_Values[f][0],
                                   var1d        = flightPoints_Values[f][1],
                                   var2d        = flightPoints_Values[f][2],
                                   var3d        = flightPoints_Values[f][3],
                                   var4d        = flightPoints_Values[f][4],
                                   repeat       = flightPoints_Values[f][5],
                                   waitTime     = flightPoints_Values[f][6])
        else: 
            self.addFlightPoint(0, root, controller)
        
        self.addNewFlightButton(root, controller)
        
        
    def onFrameConfigure(self, event):
        '''
        Reset the scroll region to encompass the inner frame
        '''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        
    def addFlightForm(self, flightID, root, controller, flightSelected = ""):
        '''
        Manage the new form to set flight parameters
        '''
        
        global flightPoints_EntryButtons
        totalRowInEachGroup = 5 #Each group has 5 rows
        firstRowIndex = len(flightPoints_EntryButtons) * totalRowInEachGroup +2 #Newly added groups will be displayed below according to this index
        
        flightLabel = ttk.Label(self.frame,
                        text = "Flight Type: ")
        flightLabel.grid(row = firstRowIndex, column = 0, sticky="E")
        
        global flightTypes
        flight_selected = tk.StringVar()
        if flightSelected == "":
            flight_selected.set(flightTypes[0])
        else:
            flight_selected.set(flightSelected)
            
        flightSelect = tk.OptionMenu(self.frame,
                                   flight_selected, 
                                   *flightTypes,
                                   command = lambda _: self.updateAll(flightID, flight_selected.get(), root, controller)
                                   ) #Source of the "lambda _:" https://stackoverflow.com/questions/35974203/optionmenu-command-function-requires-argument
                                   

        
        #flightTypes[0] should be "None"
        flightDesc = ""
        if flight_selected.get() == flightTypes[1]: #send_setpoint
            flightDesc = "Send a new control setpoint for roll/pitch/yaw/thrust to the copter"

        elif flight_selected.get() == flightTypes[2]: #send_velocity_world_setpoint
            flightDesc = "Send Velocity in the world frame of reference setpoint"
            
        elif flight_selected.get() == flightTypes[3]: #send_zdistance_setpoint
            flightDesc = "Control mode where the height is send as an absolute setpoint"
            
        elif flight_selected.get() == flightTypes[4]: #send_hover_setpoint
            flightDesc = "Control mode where the height is send as an absolute setpoint"
            
            
        flightSelect.grid(row = firstRowIndex, column = 1, columnspan = 4, sticky="WE")
        
        self.flightDescLabel = ttk.Label(self.frame)
        self.flightDescLabel.configure(text = flightDesc)
        self.flightDescLabel.grid(row = firstRowIndex, column = 5, columnspan = 6, sticky = "W")
        
        
        
    def updateAll(self, flightID, flightSelected, root, controller):
        '''
        Called when a SELECT button changes state
        '''
        global flightPoints_EntryButtons
        
        flightPoints_EntryButtons[flightID][0] = flightSelected
        saveFlightState(self)
        controller.showPage(root, flightPoints)
            
            
            
    def updateDescription(self, selectedFlight):
        '''
        Update flight description
        '''
        #flightTypes[0] should be "None"
        flightDesc = ""
        if selectedFlight == flightTypes[1]: #send_setpoint
            flightDesc = "Send a new control setpoint for roll/pitch/yaw/thrust to the copter"

        elif selectedFlight == flightTypes[2]: #send_velocity_world_setpoint
            flightDesc = "Send Velocity in the world frame of reference setpoint"
            
        elif selectedFlight == flightTypes[3]: #send_zdistance_setpoint
            flightDesc = "Control mode where the height is send as an absolute setpoint"
            
        elif selectedFlight == flightTypes[4]: #send_hover_setpoint
            flightDesc = "Control mode where the height is send as an absolute setpoint"
           
            
        self.flightDescLabel.configure(text = flightDesc)
            
    
    
    def addFlightPoint(self, 
                       flightID, root, controller,
                       flightType = "",
                       var1d = 0, 
                       var2d = 0, 
                       var3d = 0, 
                       var4d = 0,
                       repeat = 1, 
                       waitTime = 10):
        '''
        Add the form to insert a new flight point
        '''
        global flightVars
        global flightTypes
        global flightPoints_EntryButtons
        
        if flightType == "":
            flightType = flightTypes[0]
            
        self.addFlightForm(flightID, root, controller, flightType)
        self.updateDescription(flightType)
        
        totalRowInEachGroup = 5 #Each group has 5 rows
        firstRowIndex = len(flightPoints_EntryButtons) * totalRowInEachGroup +2 #Newly added groups will be displayed below according to this index
        
        
        #Separator
        horizontalSeparator = ttk.Label(self.frame, text = "")
        horizontalSeparator.grid(column = 0, columnspan = 12)
        

        var1 = var2 = var3 = var4 = ["", ""]
        
        #flightTypes[0] should be "None"
        if flightType == flightTypes[1]: #send_setpoint
            var1 = flightVars[0] #["roll",     "deg"]
            var2 = flightVars[1] #["pitch",    "deg"]
            var3 = flightVars[2] #["yaw",      "deg"]
            var4 = flightVars[3] #["thrust",   "[0, 65535]"]


        if flightType == flightTypes[2]: #send_velocity_world_setpoint
            var1 = flightVars[4] #["vx",       "m/s"]
            var2 = flightVars[5] #["vy",       "m/s"]
            var3 = flightVars[6] #["vz",       "m/s"]
            var4 = flightVars[7] #["yawrate",  "deg/s"]
            
        if flightType == flightTypes[3]: #send_zdistance_setpoint
            var1 = flightVars[0] #["roll",     "deg"]
            var2 = flightVars[1] #["pitch",    "deg"]
            var3 = flightVars[7] #["yawrate",  "deg/s"]
            var4 = flightVars[8] #["zdistance","m"]

        if flightType == flightTypes[4]: #send_hover_setpoint
            var1 = flightVars[4] #["vx",       "m/s"]
            var2 = flightVars[5] #["vy",       "m/s"]
            var3 = flightVars[7] #["yawrate",  "deg/s"]
            var4 = flightVars[8] #["zdistance","m"]
            
        
        vars12RowIndex = firstRowIndex+1
        
        #=======================================================================
        
        var1Label = ttk.Label(self.frame)
        var1Label.configure(text = var1[0] + " = ")
        var1Label.grid(row = vars12RowIndex, column = 1, sticky="E")
        
        var1_Value = var1d
        var1Entry = ttk.Entry(self.frame)
        var1Entry.insert(0, var1_Value)
        var1Entry.grid(row = vars12RowIndex, column = 2, sticky="WE")
        
        var1LabelUnit = ttk.Label(self.frame)
        var1LabelUnit.configure(text = var1[1])
        var1LabelUnit.grid(row = vars12RowIndex, column = 3, sticky="W")
        
        #=======================================================================
        
        var2Label = ttk.Label(self.frame)
        var2Label.configure(text = "            " + var2[0] + " = ")
        var2Label.grid(row = vars12RowIndex, column = 5, sticky="E")
        
        var2_Value = var2d
        var2Entry = ttk.Entry(self.frame)
        var2Entry.insert(0, var2_Value)
        var2Entry.grid(row = vars12RowIndex, column = 6, sticky="WE")
        
        var2LabelUnit = ttk.Label(self.frame)
        var2LabelUnit.configure(text = var2[1])
        var2LabelUnit.grid(row = vars12RowIndex, column = 7, sticky="W")
        
        #=======================================================================
        
        repeatLabel = ttk.Label(self.frame)
        repeatLabel.configure(text = "        Repeat: ")
        repeatLabel.grid(row = vars12RowIndex, column = 9, sticky="E")
        
        repeat_Value = repeat
        repeatEntry = ttk.Entry(self.frame)
        repeatEntry.insert(0, repeat_Value)
        repeatEntry.grid(row = vars12RowIndex, column = 10, sticky="WE")
        
        repeatLabelUnit = ttk.Label(self.frame)
        repeatLabelUnit.configure(text = "times")
        repeatLabelUnit.grid(row = vars12RowIndex, column = 11, sticky="W")
        
        
        #=======================================================================
        # 
        #=======================================================================
        
        vars34RowIndex = vars12RowIndex+2 
        
        var3Label = ttk.Label(self.frame)
        var3Label.configure(text = var3[0] + " = ")
        var3Label.grid(row = vars34RowIndex, column = 1, sticky="E")
        
        var3_Value = var3d
        var3Entry = ttk.Entry(self.frame)
        var3Entry.insert(0, var3_Value)
        var3Entry.grid(row = vars34RowIndex, column = 2, sticky="WE")
        
        var3LabelUnit = ttk.Label(self.frame)
        var3LabelUnit.configure(text = var3[1])
        var3LabelUnit.grid(row = vars34RowIndex, column = 3, sticky="W")
        
        #=======================================================================
        
        var4Label = ttk.Label(self.frame)
        var4Label.configure(text = "            " + var4[0] + " = ")
        var4Label.grid(row = vars34RowIndex, column = 5, sticky="E")
        
        var4_Value = var4d
        var4Entry = ttk.Entry(self.frame)
        var4Entry.insert(0, var4_Value)
        var4Entry.grid(row = vars34RowIndex, column = 6, sticky="WE")
        
        var4LabelUnit = ttk.Label(self.frame)
        var4LabelUnit.configure(text = var4[1])
        var4LabelUnit.grid(row = vars34RowIndex, column = 7, sticky="W")
        
        #=======================================================================
        
        waitLabel = ttk.Label(self.frame)
        waitLabel.configure(text = "        After each repetition, wait: ")
        waitLabel.grid(row = vars34RowIndex, column = 9, sticky="E")
        
        wait_Value = waitTime
        waitEntry = ttk.Entry(self.frame)
        waitEntry.insert(0, wait_Value)
        waitEntry.grid(row = vars34RowIndex, column = 10, sticky="WE")
        
        waitLabelUnit = ttk.Label(self.frame)
        waitLabelUnit.configure(text = "milliseconds")
        waitLabelUnit.grid(row = vars34RowIndex, column = 11, sticky="W")
    
    
    
        horizontalSeparator2 = ttk.Label(self.frame, text = "")
        horizontalSeparator2.grid(row = vars34RowIndex+1, column = 0, columnspan = 12)
        
        horizontalSeparator3 = ttk.Label(self.frame, text = "")
        horizontalSeparator3.grid(row = vars34RowIndex+2, column = 0, columnspan = 12)
        
        #Add the current entries to the global list of flight points
        flightPoints_EntryButtons.append(
            [
                flightType, 
                var1Entry, var2Entry, var3Entry, var4Entry, 
                repeatEntry, waitEntry
             ])
        
        
        #ADD A RESET(id)  BUTTON?
        #ADD A DELETE(id) BUTTON?
        
        
        
    
        
    def addNewFlightButton(self, root, controller):
        '''
        Button calling a specific function to save the current flight points and add a new one
        '''
        global flightPoints_Values
        rowButton = len(flightPoints_Values) * 6 + 8
        addNewGroup = ttk.Button(self.frame,
                                 text = "Add a new flight point!",
                                 command = lambda: self.addNewFlightHere(root, controller))
        addNewGroup.grid(row = rowButton, column = 3, columnspan = 6)
        
        
    def addNewFlightHere(self, root, controller):
        '''
        Enable to save the current groups and add a new one
        '''
        global flightPoints_EntryButtons
        self.addFlightPoint(len(flightPoints_EntryButtons), root, controller)
        saveFlightState(self)
        controller.showPage(root, flightPoints)

        
def saveFlightState(self):
    '''
    Save the current values of flightPoints_EntryButtons into the global list flightPoints_Values
    New instantiations of "addFlightForm" can thus be made by looking at flightPoints_Values 
        so to set the user-selected values back to the form
    Source: https://snakify.org/en/lessons/two_dimensional_lists_arrays/
    '''
    global flightTypes
    global flightPoints_EntryButtons
    global flightPoints_Values
    
    if len(flightPoints_EntryButtons) > 0:
        flightPoints_Values = []
        for id_group in range(len(flightPoints_EntryButtons)):
            supportList = []
            flightType = flightPoints_EntryButtons[id_group][0]
            
            for id_entry in range(len(flightPoints_EntryButtons[id_group])):
                if id_entry == 0: #This is the flightType
                    value = flightPoints_EntryButtons[id_group][id_entry] #It will be a string
                    
                if id_entry == 1 or id_entry == 2 or id_entry == 3 or id_entry == 4:
                    value = flightPoints_EntryButtons[id_group][id_entry].get()
                    value = validateVarsEntry(self, value)
                    
                if id_entry == 4: #This is the 4th var (thrust, yawrate, zdistance)
                    if flightType == flightTypes[1]: #In case flightType == "send_setpoint
                        value = flightPoints_EntryButtons[id_group][id_entry].get()
                        value = validateThrust(self, value)
                        
                if id_entry == 5 or id_entry == 6: #Repeat and Time to validate
                    value = flightPoints_EntryButtons[id_group][id_entry].get()
                    value = validateIntEntry(self, value)
                    
                supportList.append(value)
            flightPoints_Values.append(supportList)
            
        flightPoints_EntryButtons = []
    
    
def validateVarsEntry(self, value):
    '''
    Validate user input data
    '''
    try:
        if value[0] == "-":
            return str(0 - float(value[1:]))
        else:
            return str(float(value))
    except:
        return "0"
    
    
    
def validateIntEntry(self, value):
    '''
    Validate user input data
    '''
    try:
        if int(value) < 0:
            return "0"
        else:
            return value
    except:
        return "0"
        

def validateThrust(self, value):
    '''
    Validate user input data for the thrust
    It can range in [0, 65535]
    '''
    value = validateIntEntry(self, value)
    try:
        if int(value) > 65535:
            return "65535"
        else:
            return value
    except:
        return "65535"
    
    
class logGroups(tk.Frame):
    '''
    tk.Frame - Frame used to host the log groups
    
    ToDo List:
     - Functions to implement: 
                                 - Delete_ThisGroup(group_ID)
                                 - Save_ThisGroupToFile(g, v1, v2, v3, v4, v5, v6, t)
                                 - Load_GroupsFromFile()
                                 - Save_AllGroupsToFile()
     - Improve the logging variable choice into 2 OptionMenu: one to choose the variable's group, another to choose the variable to log
     - Improve the overall time and space performances
    '''
    
    lg_Text = "Your logging groups"
    LARGE_FONT0 = ("Verdana", 12)
    
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        label = ttk.Label(self,
                         text=self.lg_Text,
                         font=self.LARGE_FONT0,
                         justify="right")
        label.grid(row=0, column=0, columnspan = 3, sticky="EW")
        
        
        saveFlightState(self)
        
        
        #Add the right-horizontal scrollbar
        #Source: https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
        self.canvas = tk.Canvas(self, 
                                width=win_width, 
                                height=win_height,
                                borderwidth=0)
        self.frame = tk.Frame(self.canvas,
                                width=win_width, 
                                height=win_height)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.grid(row = 1, rowspan = 10, sticky="NSE")
        self.canvas.grid(row = 1, rowspan = 10, sticky="NSWE")
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)   
        
        
        #Separator
        horizontalSeparator = ttk.Label(self,
                              text = "")
        horizontalSeparator.grid(column = 0, columnspan = 10)
        

        global logGroups_Values
        totalGroups = len(logGroups_Values)
        
        if totalGroups != 0:
            for lg in range(totalGroups):
                self.addLogGroup(idGroup = lg, 
                                 name  = logGroups_Values[lg][0],
                                 var1d = logGroups_Values[lg][1],
                                 var2d = logGroups_Values[lg][2],
                                 var3d = logGroups_Values[lg][3],
                                 var4d = logGroups_Values[lg][4],
                                 var5d = logGroups_Values[lg][5],
                                 var6d = logGroups_Values[lg][6],
                                 time  = logGroups_Values[lg][7]
                                 )
        else:
            self.addLogGroup(totalGroups)
        
        self.addNewGroupButton(root, controller)
        
        
        
    def onFrameConfigure(self, event):
        '''
        Reset the scroll region to encompass the inner frame
        '''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        
        
    def addLogGroup(self, 
    				idGroup, name = "", 
					var1d = "", var2d = "", var3d = "", var4d = "", var5d = "", var6d = "", 
					time = 10):
        global logGroups_EntryButtons
        groupID = idGroup +1
        totalRowInEachGroup = 6 #Each group has 6 rows
        firstRowIndex = len(logGroups_EntryButtons) * totalRowInEachGroup +2 #Newly added groups will be displayed below according to this index
        
        #Group Form
        groupRowIndex = firstRowIndex +1
        if name == "" or name == None:
            groupText = "Group #" + str(groupID)
        else:
            groupText = name
        groupName = ttk.Entry(self.frame)
        groupName.insert(0, groupText)
        groupName.grid(row = groupRowIndex, column = 0, columnspan = 2, sticky="EW")
        
        
        #Separator
        horizontalSeparator = ttk.Label(self.frame, text = "")
        horizontalSeparator.grid(row = groupRowIndex+1, column = 0, columnspan = 10)
        
        
        #Log period
        logRowIndex = groupRowIndex +2
        logPeriod = ttk.Label(self.frame,
                              text = "Log period: ")
        logPeriod.grid(row = logRowIndex, column = 0, sticky="E")
        
        logEntry = ttk.Entry(self.frame)
        try:
            if int(time) < 10:
                basePeriod = "10"
            else:
                basePeriod = time
        except:
            basePeriod = "10"
            
        logEntry.insert(0, basePeriod)
        logEntry.grid(row = logRowIndex, column = 1)
        
        ms = ttk.Label(self.frame,
                              text = "ms")
        ms.grid(row = logRowIndex, column = 2, sticky="W")
        
        
        #Vars 1, 2 and 3
        global logVars
        varDefault = logVars[0]
        
        vars123RowIndex = groupRowIndex #Horizontally aligned with the Group Name
        var1Label = ttk.Label(self.frame,
                        text = "        Var #1: ")
        var1Label.grid(row = vars123RowIndex, column = 3, sticky="E")
        
        var1_Value = tk.StringVar()
        if var1d == "":
            var1_Value.set(varDefault)
        else:
            var1_Value.set(var1d)
        var1Entry = tk.OptionMenu(self.frame,
                                   var1_Value, 
                                   *logVars) #http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/optionmenu.html
        var1Entry.grid(row = vars123RowIndex, column = 4, columnspan = 1, sticky="WE")
        

        var2Label = ttk.Label(self.frame,
                        text = "        Var #2: ")
        var2Label.grid(row = vars123RowIndex, column = 6, sticky="E")
        
        var2_Value = tk.StringVar()
        if var2d == "":
            var2_Value.set(varDefault)
        else:
            var2_Value.set(var2d)
        var2Entry = tk.OptionMenu(self.frame,
                                   var2_Value, 
                                   *logVars)
        var2Entry.grid(row = vars123RowIndex, column = 7, columnspan = 1, sticky="WE")
        
        
        var3 = ttk.Label(self.frame,
                        text = "        Var #3: ")
        var3.grid(row = vars123RowIndex, column = 9, sticky="E")
        
        var3_Value = tk.StringVar()
        if var3d == "":
            var3_Value.set(varDefault)
        else:
            var3_Value.set(var3d)
        var3Entry = tk.OptionMenu(self.frame,
                                   var3_Value, 
                                   *logVars)
        var3Entry.grid(row = vars123RowIndex, column = 10, columnspan = 1, sticky="WE")
        
        
        #Vars 4, 5, and 6
        vars456RowIndex = logRowIndex #Horizontally aligned with the Log Period
        var4 = ttk.Label(self.frame,
                        text = "        Var #4: ")
        var4.grid(row = vars456RowIndex, column = 3, sticky="E")
        
        var4_Value = tk.StringVar()
        if var4d == "":
            var4_Value.set(varDefault)
        else:
            var4_Value.set(var4d)
        var4Entry = tk.OptionMenu(self.frame,
                                   var4_Value, 
                                   *logVars)
        var4Entry.grid(row = vars456RowIndex, column = 4, columnspan = 1, sticky="WE")
        
        
        var5 = ttk.Label(self.frame,
                        text = "        Var #5: ")
        var5.grid(row = vars456RowIndex, column = 6, sticky="E")
        
        var5_Value = tk.StringVar()
        if var5d == "":
            var5_Value.set(varDefault)
        else:
            var5_Value.set(var5d)
        var5Entry = tk.OptionMenu(self.frame,
                                   var5_Value, 
                                   *logVars)
        var5Entry.grid(row = vars456RowIndex, column = 7, columnspan = 1, sticky="WE")
        
        
        var6 = ttk.Label(self.frame,
                        text = "        Var #6: ")
        var6.grid(row = vars456RowIndex, column = 9, sticky="E")
        
        var6_Value = tk.StringVar()
        if var6d == "":
            var6_Value.set(varDefault)
        else:
            var6_Value.set(var6d)
        var6Entry = tk.OptionMenu(self.frame,
                                   var6_Value, 
                                   *logVars)
        var6Entry.grid(row = vars456RowIndex, column = 10, columnspan = 1, sticky="WE")
        
        
        horizontalSeparator2 = ttk.Label(self.frame, text = "")
        horizontalSeparator2.grid(column = 0, columnspan = 10)
        
        horizontalSeparator3 = ttk.Label(self.frame, text = "")
        horizontalSeparator3.grid(column = 0, columnspan = 10)
        
        #Add the current entries to the global list of Logging Groups
        logGroups_EntryButtons.append([groupName, var1_Value, var2_Value, var3_Value, var4_Value, var5_Value, var6_Value, logEntry])
        
        
        #ADD A RESET(id)  BUTTON?
        #ADD A DELETE(id) BUTTON?
        
        
        
        
    def addNewGroupButton(self, root, controller):
        '''
        Button calling a specific function to save the current log groups and add a new one
        '''
        addNewGroup = ttk.Button(self.frame,
                                 text = "Add a new group of variables to log!",
                                 command = lambda: self.addNewGroupHere(root, controller))
        addNewGroup.grid(column = 3, columnspan = 6)
        
        
    def addNewGroupHere(self, root, controller):
        '''
        Enable to save the current groups and add a new one
        '''
        global logGroups_EntryButtons
        
        self.addLogGroup(len(logGroups_EntryButtons))
        saveLogGroupState(self)
        controller.showPage(root, logGroups)
        
        
def saveLogGroupState(self):
    '''
    Save the current values of logGroup_EntryButtons into the global list logGroups_Values
    New instantiations of "addLogGroup" can thus be made by looking at logGroups_Values 
        so to set the user-selected values back to the form
    Source: https://snakify.org/en/lessons/two_dimensional_lists_arrays/
    '''
    global logGroups_EntryButtons
    global logGroups_Values
    
    if len(logGroups_EntryButtons) > 0:
        logGroups_Values = []
        for id_group in range(len(logGroups_EntryButtons)):
            appendThis = []
            for id_entry in range(len(logGroups_EntryButtons[id_group])):
                value = logGroups_EntryButtons[id_group][id_entry].get()
                if value == "('None',)": #Don't ask. Dunno why it computes the initial "None" in this way, but it does
                    value = "None"
                appendThis.append(value)
            logGroups_Values.append(appendThis)
            
        logGroups_EntryButtons = []
        