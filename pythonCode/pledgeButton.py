#!/usr/bin/env python3
from Adafruit_Thermal import *
import string
import random
from random import shuffle
import httplib
import urllib
import requests
import sys
import datetime
import math
import termios
import os
import csv
import time
import gps

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

TERMIOS = termios

# Excuses for GPS
excuses = ["the wrong sort of clouds!","the advent of smaller air particles!","the amount of rain!","generic topology failure.","extreme astrological conditions","the position of Venus","the fear of spoons"]

# Initialize Printer
printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

# Setup GPS
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

#Setup Http
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
passkey = ""
uniqueID = ""
credentials = []

global lat
global lng
haveGPS = False
endLat = ""
endLng = ""

#----------------------------------------------------
# Get the host, upload extension and secret key
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
    return requestHost,requestExtension,secretPOSTKey

#----------------------------------------------------
# Function to get keys
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

#-----------------------------------------------------
def shuffle_key(pass_string):
    temppass_string = list(pass_string)
    shuffle(temppass_string)
    return ''.join(temppass_string)


# Haversine formula
# Author: Wayne Dyck
#-----------------------------------------------------
def distance(origin, destination):
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
def GeneratePassword(size=15):
    randomKey = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(size)])
    return randomKey

# Print the Ticket Data
#-----------------------------------------------------
def PrintTicketInfo(unique_id,_passkey,haveGPS,_lat,_lng,_time_created):
    printer.wake()
    printer.begin(2)
    print "-----------------------------------------------------"
    print "Printing Ticket Data"
    print "-----------------------------------------------------"
    printer.feed(1)
    printer.boldOn()
    printer.println("Big Green Button")
    printer.boldOff()
    printer.feed(1)
    print "This is your id: "+unique_id;
    printer.println("Unique ID")
    printer.println(unique_id)
    print "This is your password: "+_passkey;
    printer.println("Passkey")
    printer.println(_passkey)
    if haveGPS == False:
        ex = excuses[random.randint(0,len(excuses)-1)]
        print "Unfortunately the GPS isn't working due to " + ex
        printer.println("Unfortunately the GPS isn't working due to")
        printer.println(ex)
        print "Your Pledge will be placed at Green Capital HQ"
        printer.println("Your Pledge will be placed at Green Capital HQ")
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
    printer.feed(2)

    printer.sleep()
    printer.setDefault()

# Send the Ticket Data to the Server
#-----------------------------------------------------
def SendTicketData(host,extensions,id,secretKey,passkey,haveGPS,lat,lng,time_created):
    params = {'pledge': "1","secretkey":secretKey,"pledgeid":id,"lat":lat,"lng":lng,"passkey":passkey}
    r = requests.post(host+extensions,data=params)
    print "-----------------------------------------------------"
    if r.status_code == 200:
        print "Details Sent"
    else:
        print "Houston we have a problem " + r.status_code
        print r.text

def getData():
    print "-----------------------------------------------------"
    print "Getting Info"
    lat = random.uniform(51.582492,51.348403)
    lng = random.uniform(-2.780278,-2.404524)
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print "-----------------------------------------------------"
    if haveGPS == False:
        lat = 51.414856
        lng = -2.652880
    else:
        print "We're good!"

    dst = distance((51.414856, -2.652880),(lat, lng))
    # If the gps is more the 20km away from the center point
    if dst > 20:
        print "GPS is Incorrect"
    else:
        print "GPS makes sense"

    endLat = str(lat)
    endLng = str(lng)

    passkey = GeneratePassword(15)
    seq = endLat[-3:],passkey[-5:],endLng[-3:]
    tempUniqueID = ''.join(seq)

    uniqueID = shuffle_key(pass_string=tempUniqueID)
    print "-----------------------------------------------------"
    print "Printing Ticket"
    PrintTicketInfo(unique_id=uniqueID,_passkey=passkey,haveGPS=haveGPS,_lat=endLat,_lng=endLng,_time_created=created_at);
    print "-----------------------------------------------------"
    print "Sending data to Database"
    SendTicketData(host=credentials[0],extensions=credentials[1],secretKey=credentials[2],id=uniqueID,passkey=passkey,haveGPS=haveGPS,lat=endLat,lng=endLng,time_created=created_at)

#----------------------------------------------------
def main_loop():
    while True:
        c = getkey()
        try:
            report = session.next()
            if report['class'] == 'TPV':
                print "Have GPS"
                
        except KeyError:
            pass
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            print "GPSD has terminated"

        if c == 'g':
            getData()
        time.sleep(0.1)

#----------------------------------------------------
if __name__ == '__main__':
    credentials = getSetupData()
    try:
        main_loop()
    except KeyboardInterrupt:
        printer.sleep()
        printer.wake()
        printer.setDefault()
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
