from threading import Thread, Lock

from Resourses.Singleton import SingletonMeta


class PrintThread(metaclass=SingletonMeta):

    @staticmethod
    def shared():
        return PrintThread()

    def __init__(self):
        self.end_printing_thread = False
        self.print_Lock = Lock()
        self.messages = []

    def start_print_thread(self):
        thread = Thread(target=self.print_thread)
        thread.daemon = True
        thread.start()
        thread.join(0.01)

    def append_to_message(self, message):
        self.print_Lock.acquire()
        self.messages.append(message)
        self.print_Lock.release()

    def stop_printing(self):
        self.end_printing_thread = False

    def print_thread(self):
        while not self.end_printing_thread:
            self.print_Lock.acquire()
            if self.messages:
                message = self.messages.pop(0)
                print(message)
            self.print_Lock.release()
