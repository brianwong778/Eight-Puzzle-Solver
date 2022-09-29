import time

class Timer:
    """A class whose instances store the difference between two moments in time.
    """
    def __init__(self, name=''):
        self.name = name
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()
        self.end_time = None

    def end(self):
        self.end_time = time.time()

    def get_diff(self):
        if self.start_time != None and self.end_time != None:
            return abs(self.end_time - self.start_time)
        else:
            return None

    def __repr__(self):
        return '{}: {:.5} seconds'.format(self.name, self.get_diff())
