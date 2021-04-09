import time
from multiprocessing import Process, Pipe
from threading import Thread, Lock


class ThreadingUtilities:

    def __init__(self):
        self.end_printing_thread = False
        self.print_Lock = Lock()
        self.messages = []

    def start_print_thread(self):
        x = Thread(target=self.print_thread, daemon=True)
        x.start()

    def append_to_message(self, message):
        self.print_Lock.acquire()
        self.messages.append(message)
        self.print_Lock.release()

    def print_thread(self):
        while not self.end_printing_thread:
            self.print_Lock.acquire()
            if self.messages:
                message = self.messages.pop(0)
                print(message)
            self.print_Lock.release()

    @staticmethod
    def start_new_procces_to_get_max_threads():
        parent_conn, child_conn = Pipe()
        p = Process(target=ThreadingUtilities.get_max_thread_on_machine, args=(child_conn,))
        p.start()
        while True:
            re = parent_conn.recv()
            if re != 0:
                p.terminate()
                return re - 2

    @staticmethod
    def get_max_thread_on_machine(pipe):
        threads = 0
        y = 1000000
        for i in range(y):
            try:
                x = Thread(target=lambda: time.sleep(1000), daemon=True)
                threads += 1
                x.start()
            except RuntimeError:
                break
        pipe.send(threads)
        pipe.close()
