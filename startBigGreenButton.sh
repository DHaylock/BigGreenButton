#!/bin/sh

sudo killall gpsd;
sleep(1);
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock;
cd BigGreenButton/;
pwd;

echo ls -lh;

exit 0;
