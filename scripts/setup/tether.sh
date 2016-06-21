#!/bin/bash
$ENV_ROOT/scripts/setup/tether/device.sh
sleep 3
$ENV_ROOT/scripts/setup/tether/host.sh
sleep 3
$ENV_ROOT/scripts/setup/tether/raise_interface.sh
sleep 3
$ENV_ROOT/scripts/setup/proxy/dns.sh 8.8.8.8


