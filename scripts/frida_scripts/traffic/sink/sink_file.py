class FileSink(object):
    def __init__(self, filepath):
        self._filepath = filepath
        self._handle = None

    def __enter__(self, *args, **kwargs):
        self._handle = open(self._filepath, "a")

    def __exit__(self, *args, **kwargs):
        self._handle.close()

    def write(self, data):
        self._handle.write(data)
        self._handle.flush()

    def create_subsink(self, channel):
        return self