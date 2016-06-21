import frida  
import sys  
from subprocess import Popen
import socket
from threading import Thread
import time
import os

class TrafficSnifferInjector(object):
    def __init__(self, proc):
        self.proc = proc
        
    def inject(self, traffic_sniffer):
        Popen(["adb forward tcp:27042 tcp:27042"], shell=True).wait()
        device = frida.get_device_manager().enumerate_devices()[-1]
        process = device.attach(self.proc)
        script = process.create_script(traffic_sniffer.get_sniffer_js())
        script.on('message', traffic_sniffer.on_message)
        script.load()
