#!/bin/sh
/sbin/iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
/sbin/iptables -A FORWARD -i at0 -o eth0 -j ACCEPT
