#!/bin/sh
/root/scripts/startap.sh
sleep 5
/root/scripts/setup_network.sh
sleep 5
/root/scripts/start_masq.sh
sleep 5
/root/scripts/capture_traffic.sh
service nginx restart
