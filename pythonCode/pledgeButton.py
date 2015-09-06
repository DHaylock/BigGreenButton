#!/usr/bin/env python3
# This will not work PSeudo code for the moment.
# from Adafruit_Thermal import *
import string
import random
from random import shuffle
import httplib,urllib
import sys
import datetime
import math
import Tkinter
from PIL import Image,ImageTk


# from PIL import Image, ImageTk
    # Make Window
# root = Tkinter.Tk()
# root.title("Bristol Green Capital Pledge")
# root.geometry("300x600+300+600")
# root.grid()
# root.entry = Tkinter.Entry(root)
# root.entry.grid(column=0,row=0,sticky='EW')
# LATLabelVar = Tkinter.StringVar()
# LNGLabelVar = Tkinter.StringVar()
# # Make Window
# GPSLATlabel = Tkinter.Label(root, textvariable=LATLabelVar, anchor="w",fg="black",bg="white")
# GPSLATlabel.grid(column=0,row=0,columnspan=1,sticky='EW')
# GPSLNGlabel = Tkinter.Label(root, textvariable=LNGLabelVar, anchor="w",fg="black",bg="white")
# GPSLNGlabel.grid(column=0,row=1,columnspan=1,sticky='EW')

# img = ImageTk.PhotoImage(Image.open("GreenCapitalLogo.png"))
# Tkinter.Label(root,image=img)
# photo = ImageTk.PhotoImage(image)

def shuffle_key(pass_string):
    temppass_string = list(pass_string)
    shuffle(temppass_string)
    return ''.join(temppass_string)

# Haversine formula example in Python
# Author: Wayne Dyck
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

# Excuses for GPS
excuses = ["the wrong sort of clouds!","the advent of smaller air particles!","the amount of rain!","generic topology failure.","extreme astrological conditions","the position of Venus"]

#HTTP Stuff
secretPOSTKey = "jkqcu309qivdkmv"
requestHost = "localhost:8888"
requestExtention = "/uploadPledge.php"
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

# This is the GPS
lat = random.uniform(51.582492,51.348403)
lng = random.uniform(-2.780278,-2.404524)
passkey = ""
uniqueID = ""
created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
haveGPS = True
endLat = ""
endLng = ""

# LATLabelVar.set(lat)
# LNGLabelVar.set(lng)
# Generate a New Password
def GeneratePassword(size=15):
    randomKey = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(size)])
    return randomKey

# Print the Ticket Data
def PrintTicketInfo(unique_id,_passkey,haveGPS,_lat,_lng,_time_created):
    print "-----------------------------------------------------"
    print "Printing Ticket Data"
    print "-----------------------------------------------------"
    print "This is your id: "+unique_id;
    print "This is your password: "+_passkey;
    if haveGPS == False:
        print "Unfortunately the GPS isn't working due to " + excuses[random.randint(0,len(excuses)-1)]
        print "Your Pledge will be placed at Green Capital HQ"
        print lat + ","+ lng;
    else:
        print "You Pledge location"
        print _lat+ " " +_lng;

    print "Created at: " + _time_created;
    return

# Send the Ticket Data to the Server
def SendTicketData(id,passkey,haveGPS,lat,lng,time_created):
    print "-----------------------------------------------------"
    print "Sending data to Database"
    print "-----------------------------------------------------"
    connection = httplib.HTTPConnection(requestHost)
    params = urllib.urlencode({'pledge': "1","secret":secretPOSTKey,"pledgeid":uniqueID,"lat":lat,"lng":lng,"passkey":passkey})
    connection.request("POST",requestExtention,params,headers)
    response = connection.getresponse()
    print response.status,response.reason
    print response.read()

if haveGPS == False:
    lat = "51.414856"
    lng = "-2.652880"
else:
    print "We're good!"

dst = distance((51.414856, -2.652880),(lat, lng))
# If the gps is more the 20km away from the center point
if dst > 20:
    print "GPS is Incorrect"
else:
    print "GPS makes sense"


print "-----------------------------------------------------"
print "Bristol Big Green Button"

endLat = str(lat)
endLng = str(lng)

passkey = GeneratePassword(15)
seq = endLat[-3:],passkey[-5:],endLng[-3:]
tempUniqueID = ''.join(seq)

uniqueID = shuffle_key(pass_string=tempUniqueID)

PrintTicketInfo(unique_id=uniqueID,_passkey=passkey,haveGPS=haveGPS,_lat=endLat,_lng=endLng,_time_created=created_at);
SendTicketData(id=uniqueID,passkey=passkey,haveGPS=haveGPS,lat=endLat,lng=endLng,time_created=created_at)

# root.mainloop()
