#!/bin/bash
$ENV_ROOT/scripts/setup/proxy/dns.sh 10.42.0.1
$ENV_ROOT/scripts/setup/proxy/redirect_ports.sh
$ENV_ROOT/scripts/setup/proxy/restart_dnsmasq.sh

