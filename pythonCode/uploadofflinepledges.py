import httplib
import urllib
import requests
import sys
import datetime
import math
import termios
import time
import urllib2
import csv
import json

headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
credentials = []
jsonData = []

#-----------------------------------------------------
# Get the host, upload extension and secret key
#-----------------------------------------------------
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

#-----------------------------------------------------
# Parse json
#-----------------------------------------------------
def loadJSONFile(filename):
    with open(filename,'r+') as json_file:
        json_data = json.load(json_file)

        if len(json_data) > 0:
            print("Have Data")
            jsonData = json_data
            for pledge in json_data:
                SendTicketData(host=credentials[0],extensions=credentials[1],secretKey=credentials[2],id=pledge['pledgeid'],passkey=pledge['passkey'],haveGPS=pledge['havegps'],lat=pledge['lat'],lng=pledge['lng'],time_created=pledge['created_at'])
        else:
            print("No Data to Post")
            print("Quitting")
            sys.exit(0)


        js = json.dumps(jsonData)
        z = str([])
        json_file.seek(0,0)
        json_file.write(z)
        json_file.close()

#-----------------------------------------------------
# Send the Ticket Data to the Server
#-----------------------------------------------------
def SendTicketData(host,extensions,id,secretKey,passkey,haveGPS,lat,lng,time_created):
    params = {'pledge': "","secretkey":secretKey,"pledgeid":id,"havegps":haveGPS,"lat":lat,"lng":lng,"passkey":passkey,"created_at":time_created}
    r = requests.post(host+extensions,data=params)
    print "-----------------------------------------------------"
    if r.status_code == 200:
        print "Details Sent"
    else:
        print "Houston we have a problem " + r.status_code
        print r.text

#-----------------------------------------------------
# Check there is Internet
#-----------------------------------------------------
def checkForNetwork():
    networkEscape = 1
    while (networkEscape == 1):
        try:
            urllib2.urlopen(credentials[0])
        except urllib2.URLError, e:
            networkEscape = 0
            return False
        else:
            networkEscape = 0
            return True


print("---------------------------------------")
print("Sending Saved Data")
print("---------------------------------------")
credentials = getSetupData()
if checkForNetwork() == True:
    loadJSONFile("pledges.json")
else:
    print("No Internet")

sys.exit(0)
