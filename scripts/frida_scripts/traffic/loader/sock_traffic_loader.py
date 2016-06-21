import traffic_loader_base
import json

class Subloader(object):
    def __init__(self, parent, channel):
        super(Subloader, self).__init__()
        self._parent = parent
        self._channel = channel

    def load(self, data):
        self._parent.subload(self._channel, data)

class SockTrafficLoader(traffic_loader_base.TrafficLoaderBase):        
    def __init__(self, port):
        super(SockTrafficLoader, self).__init__()
        self._port = port
        self._sock = None
    
    def create_subloader(self, channel):
        return Subloader(self, channel)

    def encode_data(self, data):
        return data.encode("base64")

    def subload(self, channel, data):
        msg = json.dumps({"data":self.encode_data(data), "channel":channel})
        self._queue.put(msg)

    def load(self, data):
    	msg = json.dumps({"data":self.encode_data(data)})
        self._queue.put(msg)