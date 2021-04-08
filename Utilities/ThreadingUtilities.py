import threading
import time
from multiprocessing import Process, Pipe


class ThreadingUtilities:

    @staticmethod
    def start_new_procces_to_get_max_threads():
        parent_conn, child_conn = Pipe()
        p = Process(target=ThreadingUtilities.get_max_thread_on_machine, args=(child_conn,))
        p.start()
        while True:
            re = parent_conn.recv()
            if re != 0:
                p.terminate()
                return re

    @staticmethod
    def get_max_thread_on_machine(pipe):
        threads = 0
        y = 1000000
        for i in range(y):
            try:
                x = threading.Thread(target=lambda: time.sleep(1000), daemon=True)
                threads += 1
                x.start()
            except RuntimeError:
                break
        pipe.send(threads)
        pipe.close()
