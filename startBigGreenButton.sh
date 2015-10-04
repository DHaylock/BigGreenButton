#!/bin/sh
echo "-------------------------------------";
echo "Starting the Big Green Button!";
echo "-------------------------------------";
echo "Kill all the GPSD processes";
sudo killall gpsd;
sudo killall gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock;
sleep 5;
echo "-------------------------------------";
echo "Start the GPSD Socket";
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock;
echo "-------------------------------------";
cd /home/pi/BigGreenButton/pythonCode/;
pwd;
python pledgeButton.py
exit 0;
