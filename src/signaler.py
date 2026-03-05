import time
import os
import signal
import subprocess
from multiprocessing import Pool
from multiprocessing import cpu_count
from ctypes import *

pid = 234710
range_max = 100000

def dispatch_sig(signal_id):
    signal_id
    # lib_dir = "../lib/siglib.a"
    lib_dir = "lib/siglib.a"
    siglib = CDLL(lib_dir)
    sig_send_val = siglib.sig_send_val
    sig_send_val.argtypes = [c_int32, c_int, c_int]
    sig_send_val.restype = c_int

    sig_send_val(int(pid), signal.SIGUSR1, signal_id)


def proc_multicore():
    count = 0

    num_cores = cpu_count()

    print(f'num_cores={num_cores}')
    pool = Pool(processes=num_cores)

    for i in range(1, range_max):
        count += 1
        # pool.apply_async(dispatch_sig )
        pool.apply_async(dispatch_sig, args=(i,))
        time.sleep(0.00125)

    pool.close()
    pool.join()

def proc_singlecore():
    for i in range(0, range_max):
        dispatch_sig(i)

def main():
    # proc_singlecore()
    proc_multicore()

if __name__ == "__main__":
    main()
