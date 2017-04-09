#!/bin/sh
airmon-ng stop mon0
airmon-ng start wlan1
echo "Launching in background, logging to airbase.log"
nohup airbase-ng --essid "xfinitywifi" -c 6 mon0 > airbase.log 2>&1 &
echo "waiting 10 seconds for interface to come up"
sleep 10
