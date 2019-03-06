'''
Created on Dec 4, 2018

@author: mark
'''

import cflib.crtp as radioChannel
import time

class findMyDrone():
    '''
    Scans the radio channel and connects to a selected drone
    '''
    
    droneURI = ""
    
    def __init__(self):
        '''
        Scans the radio channel and connects to a selected drone
        '''
        self.initializeDrivers()
        #self.scanRadioChannel() #This is not GUI intended
        #self.gui_scanForDrones()
        
        
        
    def initializeDrivers(self):
        '''
        Initialize the low-level drivers (don't list the debug drivers)
        '''
        radioChannel.init_drivers(enable_debug_driver=False)        
        
    def gui_scanForDrones(self):
        '''
        Scan the radio channel looking for drones.
        Returns a list of all the available drones
        '''
        drones = radioChannel.scan_interfaces()
        self.drones = self.removeDuplicatedDrones(drones)
        
        
    def gui_cyclicScan(self):
        '''
        Scan the radio channel looking for drones.
        Restart the scan for drones if nothing were found
        '''
        self.gui_scanForDrones()
        if len(self.drones) == 0:
            restartScanIn = 1 #seconds
            time.sleep(restartScanIn)
            #print("Restarting...\n") #DEBUG ONLY
            self.gui_cyclicScan()
        
    def removeDuplicatedDrones(self, dronesArray):
        '''
        Deletes unwanted duplicates from the available drones on the radio channel
        '''
        if len(dronesArray) == 1:
            return dronesArray
        
        sanitizeDrones = []
        unique = []
        for drone in dronesArray:
            if drone not in unique:
                sanitizeDrones.append(drone)
                unique.append(drone)
        return sanitizeDrones
    
    
                
    def get_dronesList(self):
        '''
        Return the list of available drones
        '''
        return self.drones
                
                
                
                
#===============================================================================
# Not GUI intended methods can be found below
#===============================================================================
        
    def scanRadioChannel(self):
        '''
        NOT GUI INTENDED
        Scan the radio channel looking for drones.
        If no drones are found, restarts the scan. Until the end of time.
        '''
        print('Scanning interfaces for Crazyflies...')
        
        numberDronesFound = 0
        restartScanIn = 1 #seconds
        while(numberDronesFound == 0):
            availableDrones = radioChannel.scan_interfaces() 
            availableDrones = self.removeDuplicatedDrones(availableDrones)
    
            numberDronesFound = len(availableDrones)
            if numberDronesFound == 0:
                print('No Crazyflies found, restarting scan...\n')
                time.sleep(restartScanIn)
            #   return self.scanRadioChannel()
        
        else:
            #Select all available drones, display them, let the user choose which to connect to
            print('Crazyflies found:', numberDronesFound)
            
            droneList = range(numberDronesFound)
            for i in droneList:
                print(i,") - ",availableDrones[i][0])

            try:
                chosen = int(input("Choose the Drone you want to connect to\n"))
            except ValueError:
                print("I know you can do better than that :)\n")
                return self.scanRadioChannel()
                
            if chosen not in droneList: #Now we need to check whether the input refers to a valid listed drone
                print("Bad choice indeed... I'll give you a second chance\n")
                return self.scanRadioChannel()
                    
            #Set the URI into the class variable droneURI
            #Avoid situations like: correctly find a drone to connect to but no Link/URI has been received.
            #This is usually due to low battery drone 
            if(availableDrones[0][int(chosen)] != "" or availableDrones[0][int(chosen)] != None):
                self.droneURI = availableDrones[0][int(chosen)]
            else:
                numberDronesFound = 0
                
                
                
    def get_DroneURI(self):
        '''
        NOT GUI INTENDED
        Retrieve the link to the drone
        '''
        return self.droneURI
                
                
                
                
                
                
                
                
                