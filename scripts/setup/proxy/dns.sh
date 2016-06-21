#!/bin/bash
adb shell su -c setprop net.dns1 $1 
adb shell su -c setprop net.dns2 $1
adb shell su -c setprop net.rmnet0.dns1 $1
adb shell su -c setprop net.rmnet0.dns2 $1


adb shell su -c ndc resolver flushif rndis0
adb shell su -c ndc resolver flushdefaultif
adb shell su -c ndc resolver setifdns rndis0 localdomain $1
adb shell su -c ndc resolver setdefaultif rndis0
