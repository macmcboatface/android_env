#!/bin/bash
adb shell su -c setprop ril.tethering.usb.active 1
adb shell su -c setprop sys.usb.config rndis,adb

