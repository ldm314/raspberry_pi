#!/bin/sh
echo "Bring up interface"
ifconfig at0 up
ifconfig at0 192.168.10.2 netmask 255.255.255.0

modprobe ipt_MASQUERADE

echo "Add route"
route add -net 192.168.10.0 netmask 255.255.255.0 gw 192.168.10.2
echo "Start udhcpd"
nohup udhcpd -f -S > udhcpd.log 2>&1 &

echo "Rate limiting"
/sbin/tc qdisc add dev at0 root handle 1: htb default 1
/sbin/tc class add dev at0 parent 1: classid 1:1 htb rate 1024kbit burst 5k


echo "Add firewall rules"
iptables -F FORWARD
iptables -F INPUT
iptables -F OUTPUT
iptables -P FORWARD ACCEPT
#keep them off my lan.
#iptables -I FORWARD -d 192.168.1.1 -j ACCEPT
iptables -I FORWARD -d 192.168.1.0/24 -j DROP

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE 


echo 1 > /proc/sys/net/ipv4/ip_forward
