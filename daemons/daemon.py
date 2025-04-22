import time


class Daemon:
    def __init__(self, tick_rate=10):
        self.tick_rate = tick_rate
        self.t0 = time.time()

    def sleep(self):
        sleep_time = 1 / self.tick_rate - (time.time() - self.t0)
        if sleep_time > 0:
            time.sleep(sleep_time)
        self.t0 = time.time()
