import Adafruit_DHT
import subprocess
import time
import RPi.GPIO as GPIO
import urllib.request, urllib.parse, urllib.error
import http.client
import minimalmodbus
import datetime
import serial
import serial
import pandas as pd
import numpy as np

Water1 = minimalmodbus.Instrument('/dev/ttyUSB0', 2) #port name , slave address(in decimal)
Water1.serial.baudrate                                      = 19200
Water1.serial.bytesize                                      = 8
Water1.serial.parity                                        = serial.PARITY_NONE
Water1.serial.stopbits                                      = 1
Water1.serial.timeout                                       = 1                             # secondes
Water1.mode                                                 = minimalmodbus.MODE_RTU        # rtu ou ascii // MODE_ASCII ou MODE_RTU
Water1.debug                                                = False
Water1.serial.xonxoff                                       = True
Water1.serial.rtscts                                        = False
Water1.serial.dsrdtr                                        = False
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL        = True
    

#-----------------------------------------------------------------------------------------------------------------------------------------------#
CoordinatesDict = {#Plant ID : coordinate
    "1-2-0" : "",
    "1-2-1" : "",
    "1-2-2" : "",
    "1-2-3" : "",
    "1-2-4" : "",
    "1-2-5" : "",
    "1-2-6" : "",
    "1-2-7" : "",
    "1-2-8" : "",
    "1-2-9" : "",
    "1-2-10" : "",
    "1-2-11" : "",
    "1-2-12" : "",
    "1-2-13" : "",
    "1-2-14" : "",
    "1-2-15" : "",
    "1-3-0" : "",
    "1-3-1" : "",
    "1-3-2" : "",
    "1-3-3" : "",
    "1-3-4" : "",
    "1-3-5" : "",
    "1-3-6" : "",
    "1-3-7" : "",
    "1-3-8" : "",
    "1-3-9" : "",
    "1-3-10" : "",
    "1-3-11" : "",
    "1-3-12" : "",
    "1-3-13" : "",
    "1-3-14" : "",
    "1-3-15" : "",
}
#-----------------------------------------------------------------------------------------------------------------------------------------------#
#ask hub to check which probes are plugged and convert 16bit number into an array
Water1.write_register(1, 1, 0)#array position 1 mode "plugged"
num = Water1.read_register(4,0) #fetch info about which probes are plugged (position 4 of array, 0 decimal)
plugged = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for n in range(1,17):
    bitpos = n
    plugged[n-1] = (num >> (bitpos-1))&1
#-----------------------------------------------------------------------------------------------------------------------------------------------#
        
        Plant.TotalTime = ((datetime.datetime.now() - Plant.FirstTime)/3600000)
for n in range(0,16):
    if plugged[n] == 1:
        Water1.write_register(2, n, 0) #array position 2 probe n
        time.sleep(0.04)
        Water1.write_register(1, 2, 0) #array position 1 mode measuring
        time.sleep(0.2)
        Plant.ID = (Experiment + "-" + Water1.address + "-" + Water1.read_register(2,0))#saves plant ID for dataframe for pandas and csv
        print(Plant.ID)
        Plant.AverageTemperature = Average.Temperature 
        Plant.AverageHumidity = Average.Humidity
        #--------------------------------------------------
        Plant.Coordinates = CoordinatesDict[Plant.ID]
        #--------------------------------------------------
        df2 = pd.DataFrame(Plant)
        df.append(df2)


        for y in range(1,16):#gather data for levels 1 to 15 (level 0 is reserved for plugged function and LED)
            Water1.write_register(7, y, 0)#array position 7 level y of the probe
            time.sleep(0.04)
            Water1.write_register(1, 3, 0)#array position 1 mode data transfert 
            df.at[-1, Column[6 + y]] = Water1.read_register(3,0)#fetch info about plugged detectors position 3 of array - changes value in dataframe 
            time.sleep(0.04)
            #print(Integer)
            #---Change this to write into file or cloud the values---
df.to_csv("data.csv", mode='a', index=False, header=False)
    





