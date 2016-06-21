import socket
from threading import Thread
import Queue
import subloader

class TrafficLoaderBase(Thread):
    def __init__(self):
        super(TrafficLoaderBase, self).__init__()
        self._queue = Queue.Queue()

    def load(self, msg):
        self._queue.put(msg)

    @staticmethod
    def create_loader(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def send_data(self, data):
        return NotImplemented

    def start_serving(self):
        return NotImplemented

    def run(self):
        self.start_serving()
        while True:
            data = self._queue.get()
            self.send_data(data)