import sys
import time


class TimeManager:

    def __init__(self, timeout=0):
        self.timeout = timeout
        self.start_time = TimeManager.get_time()
        self.elapsed_time = 0

    def capture_elapsed_time(self):
        now_time = TimeManager.get_time()
        self.elapsed_time = now_time - self.start_time
        return self.elapsed_time

    def is_timeout(self):
        if self.timeout - self.elapsed_time <= 0:
            return True
        else:
            return False

    @staticmethod
    def get_time():
        return time.clock() if sys.platform.startswith("win32") else time.time()

    @staticmethod
    def get_delay_in_sec(send_time, receive_time):
        return (receive_time - send_time) * 1000
