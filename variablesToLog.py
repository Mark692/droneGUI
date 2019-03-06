'''
Created on Dec 5, 2018

@author: mark
'''

from cflib.crazyflie.log import LogConfig

#You can find loggable variables in crazyflie-firmware/src/module/src/


#CONTROLLER_PID.C
controller  = ["controller.actuatorThrust", 
               "controller.roll", "controller.pitch", "controller.yaw", 
               "controller.rollRate", "controller.pitchRate", "controller.yawRate"]


#CRTP
crtp = ["crtp.rxRate", "crtp.rxDrpRte", "crtp.txRate"]


#ESTIMATOR_KALMAN.C
kalman_states = ["kalman_states.ox", "kalman_states.oy", "kalman_states.vx", "kalman_states.vy"]
kalman_pred = ["kalman_pred.predNX", "kalman_pred.predNY", "kalman_pred.measNX", "kalman_pred.measNY"]
kalman = ["kalman.inFlight", "kalman.stateX", "kalman.stateY", "kalman.stateZ", 
          "kalman.statePX", "kalman.statePY", "kalman.statePZ", "kalman.stateD0", 
          "kalman.stateD1", "kalman.stateD2", "kalman.stateSkew", "kalman.varX", 
          "kalman.varY", "kalman.varXZ", "kalman.varPX", "kalman.varPY", 
          "kalman.varPZ", "kalman.varD0", "kalman.varD1", "kalman.varD2", 
          "kalman.varSkew", "kalman.q0", "kalman.q1", "kalman.q2", "kalman.q3"]


#POSITION_CONTROLLER_PID.C
posCtl = ["posCtl.targetVX", "posCtl.targetVY", "posCtl.targetVZ", 
          "posCtl.targetX", "posCtl.targetY", "posCtl.targetZ", 
          "posCtl.Xp", "posCtl.Xi", "posCtl.Xd", 
          "posCtl.Yp", "posCtl.Yi", "posCtl.Yd", 
          "posCtl.Zp", "posCtl.Zi", "posCtl.Zd", 
          "posCtl.VXp", "posCtl.VXi", "posCtl.VXd", 
          "posCtl.VZp", "posCtl.VZi", "posCtl.VZd" ]


#POSITION_ESTIMATOR_ALTITUDE.C
#WARNING: Not recognized by the Drone!
posEstAlt = ["posEstAlt.estimatedZ", "posEstAlt.estVZ", "posEstAlt.velocityZ"]


#RANGE.C
range_c = ["range.front", "range.back", "range.up", "range.left", "range.right", "range.zrange"]


#STABILIZER.C
stabilizer  = ["stabilizer.roll", "stabilizer.pitch", "stabilizer.yaw", "stabilizer.thrust"]
acc    = ["acc.x", "acc.y", "acc.z"]
baro = ["baro.asl", "baro.temp", "baro.pressure"]
gyro    = ["gyro.x", "gyro.y", "gyro.z"]
mag    = ["mag.x", "mag.y", "mag.z"]
stateEstimate    = ["stateEstimate.x", "stateEstimate.y", "stateEstimate.z"]
ctrltarget  = ["ctrltarget.roll", "ctrltarget.pitch", "ctrltarget.yaw"]


#MISSING VARIABLES FROM:
#ATTITUDE_PID_CONTROLLER.C, CONTROLLER_MELLINGER.C, CRTP_LOCALIZATION_SERVICE.C, EXTRX.C, OUTLIERFILTER.C, sensfusion6
#---

 
#===============================================================================
# dictionary = [*controller, *crtp, 
#               *kalman_states, *kalman_pred, *kalman, 
#               *posCtl, *posEstAlt, *range_c, 
#               *stabilizer, *acc, *baro, *gyro, *mag, *stateEstimate, *ctrltarget]
#===============================================================================

#Add here all the possible logging groups available for the drone
dictionary = [*controller, 
              *kalman_states, *kalman_pred, 
              *stabilizer, *acc, *stateEstimate]

dictionary.insert(0, ["None"]) #Initial default value to display


class cluster():
    '''
    Defines a group of variables to log
    '''
    
    groupName = ""
    groupBaseName = "Group #"
    groupCounter = 0
    cf = None
    vars2log = None
    
    #This is the final result to add to the drone
    logCluster = None
    
    MIN_LOGGING_PERIOD = 10 #minimum time (in milliseconds) for each log
    groupLoggingPeriod = MIN_LOGGING_PERIOD
    
    def __init__(self, groupName, groupLoggingPeriod, *args):
        '''
        Add new variables to log and validate user input
        
        crazyFlieOBJ          = class Crazyflie Found at: cflib.crazyflie.__init__ representing the actual drone
        groupName             = name you want to give to this log group of variables
        groupLoggingPeriod    = time (in milliseconds) for the log
        *args                 = LIST of variables you wish to log
        '''
        
        #Only proceed if submitted at least 1 variable to log
        if(len(args) != 0):
            self.vars2log = args
            #self.checkArgs()
            
            self.validateInput(groupName, groupLoggingPeriod)
            self.addToLog()
        #=======================================================================
        # else:
        #     print("No variables provided! Impossible to continue")
        #=======================================================================
         
       
            
            
    def validateInput(self, groupName, groupLoggingPeriod):
        '''
        Validate Group Name and Logging Period
        Save validated value to class variables
        '''
        
        self.groupCounter += 1
        
        #Validate Group Name
        if(groupName == ""):
            self.groupName = self.groupBaseName + str(self.groupCounter)
        else:
            self.groupName = str(groupName)
        #print(self.groupName)
            
        #Validate LoggingPeriod
        try:
            if(groupLoggingPeriod <= self.MIN_LOGGING_PERIOD):
                self.groupLoggingPeriod = self.MIN_LOGGING_PERIOD
            else:
                self.groupLoggingPeriod = groupLoggingPeriod
        except:
            self.groupLoggingPeriod = groupLoggingPeriod
        #print(self.groupLoggingPeriod)
        
        
        
    def addToLog(self):
        '''
        Add the submitted variables (*args) to the self.logCluster
        '''
        
        logGroup = LogConfig(name = self.groupName, 
                            period_in_ms = self.groupLoggingPeriod) 
        
        for var2log in self.vars2log:
            for var in var2log:
                logGroup.add_variable(str(var))
        
        self.logCluster = logGroup



    def getLogConfiguration(self):
        '''
        Just return the ultimate configuration object
        '''
        return self.logCluster


         
         
    def checkArgs(self):
        '''
        Only for debug purposes
        '''
        print("Hai immesso " + str(len(self.vars2log)) + " args")
        i = 1
        for v in self.vars2log:
            print(str(i) + ") - " + str(v))
            i += 1 
