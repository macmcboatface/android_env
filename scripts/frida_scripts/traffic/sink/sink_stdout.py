import sink_dev_null
class StdoutSink(sink_dev_null.DevNullSink):
    def write(self, data):
        print data