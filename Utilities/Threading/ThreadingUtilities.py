from time import sleep
from multiprocessing import Process, Pipe
from threading import Thread, Lock
from Resourses.Singleton import SingletonMeta
from functools import reduce


class ThreadingUtilities(metaclass=SingletonMeta):

    @staticmethod
    def shared():
        return ThreadingUtilities()

    @staticmethod
    def wait(second):
        sleep(second)

    @staticmethod
    def wait_for_threads(threads, should_sleep=0):
        while True:
            maped_thread = map(lambda thread: 0 if thread.is_alive() else 1, threads)
            thread_list = list(maped_thread)
            res = reduce(lambda a, b: a + b, thread_list)
            if res == len(threads):
                sleep(should_sleep)
                return

    def keep_main_thread_alive(self):
        while not self.should_end_main_thread:
            pass

    def __init__(self):
        self.should_end_main_thread = False
        self.lock = Lock()
        self.end_printing_thread = False
        self.print_Lock = Lock()
        self.messages = []

    def end_main_thread(self):
        self.lock.acquire()
        if not self.should_end_main_thread:
            self.should_end_main_thread = True
        self.lock.release()

    @staticmethod
    def start_new_process_to_get_max_threads():
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
                x = Thread(target=lambda: sleep(1000), daemon=True)
                threads += 1
                x.start()
            except RuntimeError:
                break
        pipe.send(threads)
        pipe.close()
