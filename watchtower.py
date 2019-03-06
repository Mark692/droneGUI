'''
Created on Jan 24, 2019

@author: mark
'''
from cflib.crazyflie import Commander, Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
import time

#===============================================================================
# Esempi di utilizzo per la classe Crazyflie
#
# crazyOMG = Crazyflie().open_link("Link URI")
# crazyOMG = Crazyflie().close_link()
#===============================================================================

#===============================================================================
# Esempi di utilizzo per la classe Commander
#
# crazyflieOBJ = Crazyflie()
# commander = Commander(crazyflieOBJ)
# flightType1 = commander.send_setpoint(self, roll, pitch, yaw, thrust)
# flightType2 = commander.send_velocity_world_setpoint(self, vx, vy, vz, yawrate)
# flightType3 = commander.send_zdistance_setpoint(self, roll, pitch, yawrate, zdistance)
# flightType4 = commander.send_hover_setpoint(self, vx, vy, yawrate, zdistance)
#===============================================================================


flightTypes = [
                "None",
                "send_setpoint",
                "send_velocity_world_setpoint",
                "send_zdistance_setpoint",
                "send_hover_setpoint"
              ]



flightVars = [
                ["roll",     "deg"],        #0
                ["pitch",    "deg"],        #1
                ["yaw",      "deg"],        #2
                ["thrust",   "[0, 65535]"], #3
                ["vx",       "m/s"],        #4
                ["vy",       "m/s"],        #5
                ["vz",       "m/s"],        #6
                ["yawrate",  "deg/s"],      #7
                ["zdistance","m"]           #8
              ]


class toInfinity():
    
    def __init__(self, uriDrone, flightList):
        
        if len(flightList) != 0:
            
            #Setting up connection
            with SyncCrazyflie(uriDrone, cf = Crazyflie(rw_cache='./cache')) as scf:
                cf = scf.cf
        
                cf.param.set_value('kalman.resetEstimation', '1')
                time.sleep(0.1)
                cf.param.set_value('kalman.resetEstimation', '0')
                time.sleep(2)
            
            
                for flight in flightList:
                    if flight[0] != flightTypes[0]: #If the user selected a flight type different than None
                        
                        for repeat in range(int(flight[5])):
                            
                            if flight[0] == flightTypes[1]:
                                cf.commander.send_setpoint(float(flight[1]),
                                                           float(flight[2]),
                                                           float(flight[3]),
                                                           int(flight[4])) #Thrust
                                
                            elif flight[0] == flightTypes[2]:
                                cf.commander.send_velocity_world_setpoint(float(flight[1]),
                                                           float(flight[2]),
                                                           float(flight[3]),
                                                           float(flight[4]))
                                
                            elif flight[0] == flightTypes[3]:
                                cf.commander.send_zdistance_setpoint(float(flight[1]),
                                                           float(flight[2]),
                                                           float(flight[3]),
                                                           float(flight[4]))
                                
                                cf.commander.send_hover_setpoint(float(flight[1]),
                                                           float(flight[2]),
                                                           float(flight[3]),
                                                           float(flight[4]))
                            time.sleep(float(flight[6])/1000) #cast it to seconds
                    
                cf.commander.send_stop_setpoint()
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        