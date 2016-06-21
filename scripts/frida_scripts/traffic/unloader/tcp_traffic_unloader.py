import socket
import time
from sock_traffic_unloader import TrafficSockUnloader

class TrafficUnloaderTCP(TrafficSockUnloader):
    def __init__(self, sock, sink):
        super(TrafficUnloaderTCP, self).__init__(sock, sink)
        self._buff = ''

    def recv_data(self):
        while True:
            while True:
                try:
                    remainder, msg = self.extract_msg(self._buff)
                    self._buff = remainder
                    yield msg
                except Exception, ex:
                    break           
            self._buff += self._sock.recv(0x1000)            
    
    @staticmethod
    def create_socket(port):
        sock = socket.socket()
        try:
            sock.connect(("127.0.0.1", port))
        except Exception, ex:
            time.sleep(1)
            sock.connect(("127.0.0.1", port))
        return sock