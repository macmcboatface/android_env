import os
import socket
import Queue
from threading import Thread

class Client(Thread):
    def __init__(self, address):
        super(Client, self).__init__()
        self._sock = socket.socket()
        self._address = address
        self._queue = Queue.Queue()
        self._shouldRun = True

    def connect(self):
        self.start()

    def run(self):
        self._sock.connect(self._address)
        self.loop()

    def loop(self):
        while self._shouldRun:
            try:
                data = self._queue.get(timeout=1)
                self._sock.send(data)
            except Queue.Empty, ex:
                pass

    def signal(self, signal):
        if signal == "close":
            self._shouldRun = False

    def write(self, data):
        self._queue.put(data)


class Server(Thread):
    def __init__(self, address):
        super(Server, self).__init__()
        self._sock = socket.socket()
        self._address = address
        self._serving_sock = None
        self._serving_addr = None
        self._shouldRun = True
        self._queue = Queue.Queue()

    def write(self, data):
        self._queue.put(data)

    def serve(self):
        self.start()

    def run(self):
        self._sock.bind(self._address)
        self._sock.listen(1)
        self._serving_sock, self._serving_addr = self._sock.accept()
        self.loop()


    def loop(self):
        while self._shouldRun:
            try:
                data = self._queue.get(timeout=1)
                self._serving_sock.send(data)
            except Queue.Empty, ex:
                pass

    def signal(self, signal):
        if signal == "close":
            self._shouldRun = False


class SocketSink(object):
    def __init__(self, channel, port):
        address = ("127.0.0.1", port)
        self._client = Client(address)
        self._server = Server(address)
        self._channel = channel
        self._directions = {"incoming": self._client,
                             "outgoing":self._server}

        self._server.serve()
        self._client.connect()

    def write(self, direction, data):
        self._directions[direction].write(data)

    def signal(self, direction, signal):
        self._directions[direction].signal(signal)

    def __enter__(self, *args, **kwargs):
        pass

    def __exit__(self, *args, **kwargs):
        pass

class FactorySocketSink(object):
    def __init__(self, address):
        self._port = 2000
        self._subsinks = {}

    def create_subsink(self, channel):
        if channel not in self._subsinks:
            self._subsinks[channel] = SocketSink(channel, self._port)
            self._port += 1
        return self._subsinks[channel]

    def __enter__(self, *args, **kwargs):
        pass

    def __exit__(self, *args, **kwargs):
        pass

    def write(self, data):
        #print data
        pass