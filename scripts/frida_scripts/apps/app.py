#!/usr/bin/python
import frida_scripts.traffic.traffic as traffic
import os
import sys
import time
from frida_scripts.traffic.injector.traffic_sniffer_injector import TrafficSnifferInjector

def main(package):
    try:
        port = int(sys.argv[1])
        print "using base port : %d" % port
        outputs_dir = os.path.join("outputs", package)

        injector = TrafficSnifferInjector(package)
        sniffers = traffic.create_sniffers(port, outputs_dir)

        for sniffer in sniffers:
            injector.inject(sniffer)
        sys.stdin.read()

    except KeyboardInterrupt as e:
        sys.exit(0)

