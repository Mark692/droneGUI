
"""
Simple example that connects to the first Crazyflie found, logs the Stabilizer
and prints it to the console. After 10s the application disconnects and exits.
"""
import logging
import time
import Connection
import cflib.crtp  as radioChannel # noqa
from variablesToLog import cluster as clusterLog

from cflib.crazyflie import Crazyflie
from threading import Timer
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

#from LogData import Log


# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)



class LoggingExample:
    """
    Simple logging example class that logs the Stabilizer from a supplied
    link uri and disconnects after 5s.
    """

    logGroup = []
    log = None
    
    #To log multiple groups at the same time it should be considered to 
    #make this class iterable
    
    def __iter__(self):
        return self
    
    def __next__(self):
        None
    
    
    def __init__(self, droneLink, toLog = [], disconnected_delay = 3):
        """
        Initialize and run the example with the specified droneLink 
        """
        if(droneLink != ""):
            self._cf = Crazyflie(rw_cache='./cache')
            
            #===================================================================
            # self.addNewLogGroup("Stime di Stato", 50, "")00
            # self.addNewLogGroup("Coordinate", 10, "gps.lat", "gps.lon")
            #===================================================================
            #self.addNewLogGroup("Pressione", 500,"baro.pressure")
            self.logGroup = toLog
            
            
            # Connect some callbacks from the Crazyflie API
            self._cf.connected.add_callback(self._connected)
            self._cf.disconnected.add_callback(self._disconnected)
            self._cf.connection_failed.add_callback(self._connection_failed)
            self._cf.connection_lost.add_callback(self._connection_lost)

    
            # Try to connect to the Crazyflie
            self._cf.open_link(droneLink)
    
            # Variable used to keep main loop occupied until disconnect
            self.is_connected = True
            
            self.delayedDisconnectDrone(disconnected_delay)
            

    def addNewLogGroup(self, groupName, loggingPeriod, *args):
        '''
        Add the *args to log
        '''
        toLog = clusterLog(self._cf, groupName, loggingPeriod, *args)
        self.logGroup.append(toLog.getLogConfiguration())



    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
        print('Connected to %s' % link_uri)
        
        for addMe in self.logGroup:
            
            # Adding the configuration cannot be done until a Crazyflie is
            # connected, since we need to check that the variables we
            # would like to log are in the TOC.
            try:
                self._cf.log.add_config(addMe)
    
                # This callback will receive the data
                
                title = addMe.name
                gotError = True
                while gotError:
                    try:
                        self.log = open("./Logs/" + str(time.time()) + " - " + title, 'x')
                        gotError = False
                    except:
                        title += "_"
                        
                        
                addMe.data_received_cb.add_callback(self._stab_log_data)

                # This callback will be called on errors
                addMe.error_cb.add_callback(self._stab_log_error)
    
                # Start the logging
                addMe.start()
            except KeyError as e:
                print('Could not start log configuration,'
                      '{} not found in TOC'.format(str(e)))
                #self.log.closeLog()
            except AttributeError:
                print('Could not add ' + addMe.name + ' to logCluster, bad configuration.')
                    
                
        

    def _stab_log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        print('Error when logging %s: %s' % (logconf.name, msg))
        
        

    def _stab_log_data(self, timestamp, data, logconf):
        """Callback froma the log API when data arrives"""
        
        self.log.write('[%d][%s]: %s' % (timestamp, logconf.name, data) + "\n")
        print('[%d][%s]: %s' % (timestamp, logconf.name, data))


    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the speficied address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))
        self.is_connected = False
        self.log.close()
        
        

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))
        self.log.close()



    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)
        self.is_connected = False
        


    def disconnectDrone(self):
        '''
        Disconnect the drone
        '''
        self.drone.close_link()
        
        
        
    def delayedDisconnectDrone(self, delay):
        '''
        Disconnect the drone after a delay (in seconds)
        '''
        Timer(delay, self._cf.close_link).start()
        
        try:
            self.log.close()
        except:
            None
        
        