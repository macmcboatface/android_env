#!/bin/bash
export USB_DEVICE=`$ENV_ROOT/scripts/utils/get_device_interface.sh`
$ENV_ROOT/scripts/utils/redirect_port.sh $USB_DEVICE 80 8080
$ENV_ROOT/scripts/utils/redirect_port.sh $USB_DEVICE 443 8080
$ENV_ROOT/scripts/utils/redirect_port.sh $USB_DEVICE 5228 9090
