#!/bin/bash
adb push $ENV_ROOT/tools/binaries/device /data/local/tmp/bin
adb shell chmod -R 755 /data/local/tmp/bin

adb push $ENV_ROOT/scripts/device /data/local/tmp/scripts
adb shell chmod -R 755 /data/local/tmp/scripts

adb shell su -c /data/local/tmp/scripts/clear_rmnet_routes.sh

