import os
import time
import signal
from ctypes import *
from queue import Queue
from logging.handlers import RotatingFileHandler
import traceback
import threading
# import logger


max_sig = 100000

queue_outbox = Queue(100000)


class SignalProcessor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._queue_outbox = Queue(100000)
        self._shutdown = False
        self._is_shutdown = False
        self._shutdown_flag = threading.Event()
        self.my_function = CFUNCTYPE(None, c_int)
        self.callback_ptr = self.my_function(self.enqueue_signal)


        self.MAX_VAL = 100000

    def run(self):
        print("sigmon_outbox")
        print(f' - pid={os.getpid()}')
        print("    - SignalProcessor(Thread)")
        print(f'     - native-id={threading.get_native_id()}')
        print(f'     - ident={threading.get_ident()}')
        print(f'     - status=running')
        self.siglib = CDLL('./lib/siglib.a') # For server instance
        self.set_handler = self.siglib.sig_set_handler
        self.set_handler.argtypes = [c_int, self.my_function]
        self.set_handler.restype = None
        self.set_handler(signal.SIGUSR1, self.callback_ptr)
        while not self._shutdown_flag.is_set():
            try:
                if(self._queue_outbox.qsize() > 0):
                    sig_val = self._queue_outbox.get(True)
                    self._queue_outbox.task_done()
                    print(f'sig_val: val: {self.MAX_VAL-sig_val}')

                time.sleep(.00125)
                pass
            except Exception as e:
                print(e)
                break
                pass
            finally:
                pass
    def enqueue_signal(self, value):
        self._queue_outbox.put(value, block=True, timeout=1)


def enqueue_signal(value):
    # print(f'signal_enqueue: val: {value}')
    print(f'signal_enqueue: val: {max_sig-value}')
    queue_outbox.put(value, block=True, timeout=1)
    # self._log.debug("signal enqueue value: ({})".format(value))
    # self._queue.put(value, block=True, timeout=1)

def exec():
    my_function = CFUNCTYPE(None, c_int)
    # callback_ptr = my_function(self. enqueue_signal)
    callback_ptr = my_function(enqueue_signal)
    # siglib = CDLL('lib/siglib.a') # IMPORTANT: FOR DEV DOCKER ONLY
    siglib = CDLL('./lib/siglib.a') # For server instance
    set_handler = siglib.sig_set_handler
    set_handler.argtypes = [c_int, my_function]
    set_handler.restype = None

    set_handler(signal.SIGUSR1, callback_ptr)

    while(True):
        time.sleep(.025)

def exec_thread():
    sig_proc = SignalProcessor()
    sig_proc.start()
    while(True):
        time.sleep(1)

def main():
    exec_thread()

if __name__ == "__main__":
    main()

