import frida  
import sys  
from subprocess import Popen
import socket
from threading import Thread
import time
import os

class Sniffer(object):
	def __init__(self, loaders, unloaders):
		self._loaders = loaders
		self._unloaders = unloaders

	@staticmethod
	def create_sniffer(sniffer_cls, base_port, output_dir):
		loaders = sniffer_cls._create_loaders(base_port)
		unloaders = sniffer_cls._create_unloaders(base_port, output_dir)
		return sniffer_cls(loaders, unloaders), base_port+len(loaders)

