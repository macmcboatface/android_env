import json
import traffic_unloader

class TrafficSockUnloader(traffic_unloader.TrafficUnloaderBase):
    def __init__(self, sock, sink):
        super(TrafficSockUnloader, self).__init__(sock , sink)
       
    def handle_data(self, data):
        msg = data
        data = msg["data"]
        if "channel" in msg:
            channel = msg["channel"]
            sink = self._traffic_sink.create_subsink(channel)
        else:
            sink = self._traffic_sink
        with sink:
            sink.write(data)

    def decode_msg(self, data):
        msg = json.loads(data)
        msg["data"] = self.decode_data(msg["data"])
        return msg

    def decode_data(self, data):
        return data.decode("base64")

    def extract_msg(self, raw_data):
        if raw_data == '':
            raise Exception("WTF!")
        if raw_data[0] != "{":
            raise Exception("WTF!")
        if "}" not in raw_data:
            raise Exception("WTF!")

        ind = raw_data.find("}")
        data = raw_data[:ind+1]

        remainder = raw_data[ind+1:]
        msg = self.decode_msg(data)
        return remainder, msg
