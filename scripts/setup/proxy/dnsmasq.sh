#!/bin/bash
sudo dnsmasq --conf-file=$ENV_ROOT/conf/dnsmasq.conf --no-hosts --hostsdir=$ENV_ROOT/conf/hosts/   --listen-address=10.42.0.1
