import socket
import sock_traffic_loader

class TrafficLoaderUDP(sock_traffic_loader.SockTrafficLoader):
    def send_data(self, data):
        self._sock.sendto(data, self._addr)

    def start_serving(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._addr = ("127.0.0.1", self._port)