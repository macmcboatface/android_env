#!/bin/bash
sudo ifconfig `$ENV_ROOT/scripts/utils/get_device_interface.sh` 10.42.0.1 netmask 255.255.255.0
sudo sysctl net.ipv4.ip_forward=1
sudo iptables -t nat -F
sudo iptables -t nat -A POSTROUTING -j MASQUERADE

