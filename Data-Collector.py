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

class Data:
    def __init__(self,ID,Coordinates,FirstTime,TotalTime,Iteration,AverageTemperature,AverageHumidity,Moisture1,Moisture2,Moisture3,Moisture4,Moisture5,Moisture6,Moisture7,Moisture8,Moisture9,Moisture10,Moisture11,Moisture12,Moisture13,Moisture14,Moisture15):
        self.ID = ID #plant ID = Experiment#-Slave#-Probe#  "Experiment"+"-"+"Water1.address"+"-"+"ProbeNumber"
        self.Coordinates = Coordinates #for plotly-Dash
        self.FirstTime = FirstTime #Time and date experiment started
        self.TotalTime = TotalTime,#current time and date
        self.Iteration = Iteration#increments when watered
        self.AverageTemperature = AverageTemperature#takes average temperature from csv file based on Division variable
        self.AverageHumidity = AverageTemperature#takes average Humidity from csv file based on Division variable
        self.Moisture1 = Moisture1#current humidities
        self.Moisture2 = Moisture2
        self.Moisture3 = Moisture3
        self.Moisture4 = Moisture4
        self.Moisture5 = Moisture5
        self.Moisture6 = Moisture6
        self.Moisture7 = Moisture7
        self.Moisture8 = Moisture8
        self.Moisture9 = Moisture9
        self.Moisture10 = Moisture10
        self.Moisture11 = Moisture11
        self.Moisture12 = Moisture12
        self.Moisture13 = Moisture13
        self.Moisture14 = Moisture14
        self.Moisture15 = Moisture15
Plant = Data(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
#--------------------------------------------------------------------------------------------------------------------------------------

def Plugged():#ask hub to check which probes are plugged and convert 16bit number into an array
    Water1.write_register(1, 1, 0)#array position 1 mode "plugged"
    num = Water1.read_register(4,0) #fetch info about which probes are plugged (position 4 of array, 0 decimal)
    plugged = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for n in range(1,17):
        bitpos = n
        plugged[n-1] = (num >> (bitpos-1))&1
#-----------------------------------------------------------------------------------------------------------------------------------------------#
        
        Plant.TotalTime = ((datetime.datetime.now() - Plant.FirstTime)/3600000)
def DataTransfer():
    Plugged()
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
    df.to_csv("data.csv", mode='a', index=False, header=False)
#-----------------------------------------------------------------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------------------------------------------------------------#
class Averages:
    def __init__(self, Temperature, Humidity, CurrentTime):
        self.Temperature = Temperature
        self.Humidity = Humidity
        self.CurrentTime = CurrentTime
Average = Average(0,0,0)

def AVGHT():
    
        Average.CurrentTime = datetime.datetime.now()
    for x in range ( (Average.CurrentTime.hour - (24 - (1 + Division))), (Average.CurrentTime.hour + 1) ):
        Average.Temperature = (Average.Temperature + df.at[x, "Temperature"])
        Average.Humidity = (Average.Humidity + df.at[x, "Humidity"])
    Average.Temperature = round(Average.Temperature / Division)
    Average.Humidity = round(Average.Humidity / Division)
#-----------------------------------------------------------------------------------------------------------------------------------------------#

def RS485Probing(Division, CheckPointHour, CheckPoint):
    t = datetime.datetime.now()
        
    if t.hour = (CheckPointHour * CheckPoint) and CheckPoint < Division:
        AVGHT()
        DataTransfer():
        
        CheckPoint += 1

    elif t.hour =! (CheckPointHour * CheckPoint) and CheckPoint < Division:
        pass #nothing to do
    
    elif CheckPoint >= Division:
        CheckPoint = 0# reset time to 0h format



#------------------------------------------------------------------------------------
#will ask if initial time is needed when  module is imported
Beggining = input('Take absolute beggining [y/n]:')
if Beggining == 'y':
    Plant.FirstTime = datetime.datetime.now()
    #add info about plant ID
else:
    Plant.FirstTime = df.at[-1, "FirstTime"]
