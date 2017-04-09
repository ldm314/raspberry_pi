#!/bin/sh
brctl addbr FREE-WIFI-bridge
brctl addif FREE-WIFI-bridge eth0
brctl addif FREE-WIFI-bridge at0
ifconfig eth0 0.0.0.0 up
ifconfig at0 0.0.0.0 up
echo 1 > /proc/sys/net/ipv4/ip_forward
