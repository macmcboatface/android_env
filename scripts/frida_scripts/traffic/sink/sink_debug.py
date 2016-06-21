class DebugSink(object):
    def __init__(self, filepath):
        self._msgs = []

    def __enter__(self, *args, **kwargs):
        pass

    def __exit__(self, *args, **kwargs):
        pass

    def write(self, data):
        self._msgs.append(data)