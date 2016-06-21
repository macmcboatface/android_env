class DevNullSink(object):
    def __init__(self, filepath):
        pass

    def __enter__(self, *args, **kwargs):
        pass

    def __exit__(self, *args, **kwargs):
        pass

    def write(self, data):
        pass