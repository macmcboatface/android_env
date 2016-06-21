import os
import sink_file

class DirSink(object):
    def __init__(self, filepath):
        self._filepath = filepath
        if not os.path.exists(self._filepath):
            os.makedirs(self._filepath)
        self._handle = None
        self._counter = 0
        self._subsinks = {}

    def __enter__(self, *args, **kwargs):
        self._handle = open(os.path.join(self._filepath, str(self._counter)), "wb")
        self._counter += 1

    def __exit__(self, *args, **kwargs):
        self._handle.close()

    def write(self, data):
        self._handle.write(data)

    def create_subsink(self, channel):
        if channel not in self._subsinks:
            self._subsinks[channel] = sink_file.FileSink(os.path.join(self._filepath, channel)) 
        return self._subsinks[channel]