import Adafruit_DHT
import subprocess
import time
import RPi.GPIO as GPIO
import urllib.request, urllib.parse, urllib.error
import http.client
import minimalmodbus
import datetime
import serial

class Measurements:
    def __init__(self, Temperature, Humidity, CurrentTime, Hour):
        self.Temperature = Temperature
        self.Humidity = Humidity
        self.CurrentTime = CurrentTime
        self.Hour = Hour

room = Measurements(0,0,0,18)

def SBG_DHT(room):
    
    room.CurrentTime = datetime.datetime.now()

    if room.CurrentTime.hour >= room.Hour  and room.Hour < 24:
        print(room.CurrentTime.hour)
        print(room.Hour)
        sensor = Adafruit_DHT.DHT22
        pin = 4
        room.Humidity, room.Temperature = Adafruit_DHT.read_retry(sensor, pin) #get temperature
        #print("\033[1;31;40m \n", 'Temp={0:0.1f}*C'.format(room.Temperature))
        #print("\033[1;35;40m \n", 'humidity={0:0.1f}%'.format(room.Humidity))
        room.Hour += 1

    elif room.CurrentTime.hour < Hour  and room.Hour < 24:
        pass #do nothing
    
    elif room.Hour >= 24:
        room.Hour = 0 #reset time to 0h format

#----------------------------------------------------------------------------------------------

while True:
    SBG_DHT(room)
    time.sleep(5)

class Data:
    def __init__(self,ID,Coordinates,FirstTime,TotalTime,Iteration,AverageTemperature,AverageHumidity,Moisture1,Moisture2,Moisture4,Moisture5,Moisture6,Moisture7,Moisture8,Moisture9,Moisture10,Moisture11,Moisture12,Moisture13,Moisture14,Moisture15,):
        
        self.ID = ID #plant ID = Experiment#-Slave#-Probe#
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



            


