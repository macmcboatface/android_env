import frida  
import sys  
from subprocess import Popen
import socket
from threading import Thread
import time
import os

class TrafficUnloaderBase(Thread):
    def __init__(self, sock, sink):
        Thread.__init__(self)
        self._sock = sock
        self._traffic_sink = sink
       
    def run(self):
        for data in self.recv_data():
            self.handle_data(data)

    def handle_data(self, data):
        with self._traffic_sink:
            self._traffic_sink.write(data)
    
    def recv_data(self):
        return NotImplemented

    @staticmethod
    def create_socket(outgoing_port, incoming_port):
        return NotImplemented

    @staticmethod
    def create_unloader(unloader_cls, src, sink):
        return unloader_cls(unloader_cls.create_socket(src), sink)

    @staticmethod
    def create_unloaders(unloader_cls, unloading_defs):
        unloaders = []
        for src, sink in unloading_defs:
            unloaders.append(unloader_cls.create_unloader(unloader_cls, src, sink))
        return unloaders