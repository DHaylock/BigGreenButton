#!/usr/bin/env python3
from Adafruit_Thermal import *
import string
import random
from random import shuffle
import RPi.GPIO as GPIO
import httplib
import urllib
import requests
import Image
import sys
import datetime
import math
import termios
import os
import csv
import time
import urllib2
from gps import *
import threading

jsonData = []
haveInternet = False
networkEscape = 1

print "-----------------------------------------------------"
print """
  ____  _          _____                       ____        _   _
 |  _ \(_)        / ____|                     |  _ \      | | | |
 | |_) |_  __ _  | |  __ _ __ ___  ___ _ __   | |_) |_   _| |_| |_ ___  _____
 |  _ <| |/ _  | | | |_ |  __/ _ \/ _ \ '_ \  |  _ <| | | | __| __/ _ \|  _  |
 | |_) | | (_| | | |__| | | |  __/  __/ | | | | |_) | |_| | |_| || (_) | | | |
 |____/|_|\__, |  \_____|_|  \___|\___|_| |_| |____/ \____|\__|\__\___/|_| |_|
           __/ |
          |___/                                                               """

print "-----------------------------------------------------"

# GPSPoller
#----------------------------------------------------
class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()

gpsd = None #seting the global variable

global lat
global lng
haveGPS = False
endLat = ""
endLng = ""

# For debugging
TERMIOS = termios

#Setup Http
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
passkey = ""
uniqueID = ""
credentials = []

# Setup Button
buttonPin = 12
relayPin = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(relayPin, GPIO.OUT)

# Button Pushed Flag
buttonPushed = False

# Get the host, upload extension and secret key
#----------------------------------------------------
def getSetupData():
    secretPOSTKey = ""
    requestHost = ""
    requestExtension = ""
    with open("info.csv","rb") as f:
        reader = csv.DictReader(f)
        for row in reader:
            requestHost = row['Host']
            requestExtension = row['Request']
            secretPOSTKey = row['Secret']

    print "-----------------------------------------------------"
    print "Hostname: %s" % requestHost
    print "Extension: %s" % requestExtension
    print "Secret Key: %s" % secretPOSTKey
    print "-----------------------------------------------------"
    return requestHost,requestExtension,secretPOSTKey

# Function to get keys
#----------------------------------------------------
def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
            c = os.read(fd, 1)
    finally:
            termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c

# Shuffle the Values
#-----------------------------------------------------
def shuffle_key(pass_string):
    temppass_string = list(pass_string)
    shuffle(temppass_string)
    return ''.join(temppass_string)

# Haversine formula
# Author: Wayne Dyck
#-----------------------------------------------------
def checkDistance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

# Generate a New Password
#-----------------------------------------------------
def GeneratePassword(size=8):
    randomKey = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(size)])
    return randomKey

# Print the Ticket Data
#-----------------------------------------------------
def PrintTicketInfo(unique_id,_passkey,haveGPS,_lat,_lng,_time_created):
    print "Printing Ticket Data"
    print "-----------------------------------------------------"
    printer.feed(1)
    printer.setSize('L')
    printer.justify('C')
    printer.println("Big Green Button")
    printer.feed(1)
    printer.printImage(Image.open('logo.png'), False)
    printer.justify('L')
    printer.setSize('S')
    print "This is your id: "+unique_id;
    printer.justify('C')
    printer.println("Unique ID")
    printer.println(unique_id)
    printer.feed(1)
    print "This is your password: "+_passkey;
    printer.justify('C')
    printer.println("Passkey")
    printer.println(_passkey)
    printer.feed(1)
    printer.justify('L')
    if haveGPS == False:
        GPSLine = "The GPS didnt Work!"
        print GPSLine
        printer.println(GPSLine)
        print "Your Pledge is at Green Capital HQ"
        printer.println("Your Pledge at Green Capital HQ")
        print _lat + ","+ _lng;
        printer.println("Lat: "+_lat)
        printer.println("Lng: "+_lng)
    else:
        print "Your Pledge Location"
        print _lat+ " " +_lng;
        printer.println("Your Pledge Location")
        printer.println("Lat: "+_lat)
        printer.println("Lng: "+_lng)

    print "Created at: " + _time_created;
    printer.println("Created at: " + _time_created)
    printer.feed(1)
    printer.justify('C')
    printer.println("Please Visit")
    printer.println("http://Someurl.co.uk")
    printer.println("And make your pledge!")
    printer.feed(2)

# Send the Ticket Data to the Server
#-----------------------------------------------------
def SendTicketData(host,extensions,id,secretKey,passkey,haveGPS,lat,lng,time_created):
    params = {'pledge': "1","secretkey":secretKey,"pledgeid":id,"havegps":haveGPS,"lat":lat,"lng":lng,"passkey":passkey,"created_at":time_created}

    if haveInternet == True:
        r = requests.post(host+extensions,data=params)
        print "-----------------------------------------------------"
        if r.status_code == 200:
            print "Details Sent"
        else:
            print "Houston we have a problem " + r.status_code
            print r.text
    elif haveInternet == False:
        print "No Internet"
        saveToJSONFile(filename="pledges.json",params=params)



#-----------------------------------------------------
# Parse json
#-----------------------------------------------------
def saveToJSONFile(filename,params):
    with open(filename,'r+') as json_file:
        json_data = json.load(json_file)
        js = params
        jsonData.append(js)

        js = json.dumps(jsonData)
        print(js)
        z = str(json.dumps(jsonData,indent=4, separators=(',', ': ')))
        # json_file.seek(0,0)
        json_file.write(z)
        json_file.close()
# Get the Data
#-----------------------------------------------------
def getData(_lat,_lon,_fix):

    print "-----------------------------------------------------"
    print "Getting Info"
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print "-----------------------------------------------------"
    if _fix == False:
        print "No GPS"
    else:
        print "Have GPS"

    dst = checkDistance((51.414856, -2.652880),(_lat, _lon))

    # If the gps is more the 20km away from the center point
    if dst > 20:
        print "GPS is Incorrect"
    else:
        print "GPS makes sense"

    endLat = str(_lat)
    endLng = str(_lon)

    passkey = GeneratePassword(7)
    seq = endLat[-2:],passkey[-2:],endLng[-2:]
    tempUniqueID = ''.join(seq)

    uniqueID = shuffle_key(pass_string=tempUniqueID)

    pushed = True
    if pushed == True:
        print "-----------------------------------------------------"
        print "Printing Ticket"
        PrintTicketInfo(unique_id=uniqueID,_passkey=passkey,haveGPS=_fix,_lat=endLat,_lng=endLng,_time_created=created_at);
        print "-----------------------------------------------------"
        print "Sending data to Database"
        SendTicketData(host=credentials[0],extensions=credentials[1],secretKey=credentials[2],id=uniqueID,passkey=passkey,haveGPS=_fix,lat=endLat,lng=endLng,time_created=created_at)
        pushed = False

# Main Loop
#----------------------------------------------------
def main_loop():
    global lat
    global lng

    while True:
        input_state = GPIO.input(buttonPin)
        if input_state == False:

            print('Button Pressed')
            if gpsd.fix.mode == 0:
                haveGPS = False
                print 'No GPS'
                lat = 51.4513363  #random.uniform(51.582492,51.348403)
                lng = -2.5982121 #random.uniform(-2.780278,-2.404524)
                getData(_lat=lat,_lon=lng,_fix=haveGPS)

            elif gpsd.fix.mode == 1:
                haveGPS = False
                print 'No Fix'
                lat = 51.4513363
                lng = -2.5982121
                getData(_lat=lat,_lon=lng,_fix=haveGPS)

            elif gpsd.fix.mode == 2 | 3:
                haveGPS = True
                print 'Found a Fix'
                print
                print ' GPS reading'
                print '|----------------------------------------|'
                print '| Latitude     |' , gpsd.fix.latitude
                print '| Longitude    |' , gpsd.fix.longitude
                print '| Time utc     |' , gpsd.utc,' + ', gpsd.fix.time
                print '| Altitude (m) |' , gpsd.fix.altitude
                print '| Eps          |' , gpsd.fix.eps
                print '| Epx          |' , gpsd.fix.epx
                print '| Epv          |' , gpsd.fix.epv
                print '| Ept          |' , gpsd.fix.ept
                print '| Speed (m/s)  |' , gpsd.fix.speed
                print '| Climb        |' , gpsd.fix.climb
                print '| Track        |' , gpsd.fix.track
                print '| Mode         |' , gpsd.fix.mode
                print '| Sats         |' , gpsd.satellites
                print '|----------------------------------------|'
                lat = gpsd.fix.latitude
                lng = gpsd.fix.longitude
                getData(_lat=lat,_lon=lng,_fix=haveGPS)

        time.sleep(0.5)

# Run
#----------------------------------------------------
if __name__ == '__main__':
    # Just in case flip the relay to off wait then turn on
    GPIO.output(relayPin, False)
    time.sleep(1)
    GPIO.output(relayPin, True)
    time.sleep(2)

    # Do this setup
    credentials = getSetupData()

    # Initialize Printer
    printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
    printer.sleep()
    time.sleep(1)
    printer.feed(1)
    printer.println("---------------------------")
    printer.println("Initialized")
    printer.println("Printer Connected")
    printer.println(credentials[0])
    printer.println(credentials[1])
    while (networkEscape == 1):
        try:
            urllib2.urlopen(credentials[0])
        except urllib2.URLError, e:
            printer.println("Not Connected to Internet")
            haveInternet = False
            time.sleep(5)
        else:
            printer.println("Connected to Internet")
            haveInternet = True
            networkEscape = 0
    printer.println("---------------------------")
    printer.feed(1)

    gpsp = GpsPoller()
    gpsp.start()

    try:
        main_loop()
    except KeyboardInterrupt:
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join()
        printer.sleep()
        GPIO.output(relayPin, False)
        time.sleep(1)
        GPIO.cleanup()
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
