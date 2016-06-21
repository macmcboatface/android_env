import socket
import time
from sock_traffic_unloader import TrafficSockUnloader

class TrafficUnloaderUDP(TrafficSockUnloader):
    def recv_data(self):
        data, addr = self._sock.recvfrom(0x1000)
        return data
    
    @staticmethod
    def create_socket(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.bind(("127.0.0.1", port))
        except Exception, ex:
            time.sleep(1)
            sock.bind(("127.0.0.1", port))
        return sock