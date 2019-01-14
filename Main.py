
import subprocess
import time
import RPi.GPIO as GPIO
import urllib.request, urllib.parse, urllib.error
import http.client
import minimalmodbus
import datetime
import serial
import rs485V10 #don't forget to change name of other module with actual function for lights
import rs485V3BPandas
import THAverages

start = 21
end = start +10
Connect = 0
Division = 2
CheckPoint = 0
CheckPointHour = 24 / Division

while True:
    
    if Connect == 5:
        print ("Device X not connected")
    try:
        rs485V10.LightOne(start,end)#look if lights need to be turned ON/OFF
        SBG_DHT(room)#looks if measurments need to be taken for Temperature and humidity
        RS485Probing(Division, CheckPointHour, CheckPoint)
        
        
    except ValueError as error:
        Connect = Connect + 1
        print("not connected")
    
    time.sleep(5)

