#!/bin/bash
adb shell su -c ifconfig rndis0 10.42.0.2 netmask 255.255.255.0
adb shell su -c route add default gw 10.42.0.1 dev rndis0

adb shell su -c /data/local/tmp/scripts/clear_rmnet_routes.sh
