import socket
import sock_traffic_loader

class TrafficLoaderTCP(sock_traffic_loader.SockTrafficLoader):
    def send_data(self, data):
        self._sock.send(data)

    def start_serving(self):
        sock = socket.socket()
        addr = ("127.0.0.1", self._port)
        sock.bind(addr)
        sock.listen(1)
        self._sock, self._addr = sock.accept()
