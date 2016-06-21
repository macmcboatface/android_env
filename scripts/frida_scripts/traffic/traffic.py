import os
from sniffer.ssl_java_sniffer import SSLJavaSniffer
from sniffer.ssl_socket_sniffer import SocketSniffer
from sniffer.finsky_log_sniffer import FinskyLogSniffer
from injector.traffic_sniffer_injector import TrafficSnifferInjector


#SNIFFERS = [SSLJavaSniffer, FinskyLogSniffer, SocketSniffer]
#SNIFFERS = [SSLJavaSniffer, FinskyLogSniffer]
SNIFFERS = [SocketSniffer]

def create_sniffers(base_port, outputs_dir):
    next_port = base_port
    sniffers = []
    for sniffer_cls in SNIFFERS:
        sniffer_outputs_path = os.path.join(outputs_dir, sniffer_cls.__name__)
        if not os.path.exists(sniffer_outputs_path):
            os.makedirs(sniffer_outputs_path)
        sniffer, last_port = sniffer_cls.create_sniffer(sniffer_cls, next_port, sniffer_outputs_path)
        sniffers.append(sniffer)
        next_port = last_port + 1
    return sniffers