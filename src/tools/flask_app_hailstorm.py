import requests

from multiprocessing import Pool
from multiprocessing import cpu_count

BASE_URI = "http://localhost:5001/ident"

def dispatch_request():
    resp = requests.get(BASE_URI)
    print(resp)

def proc_singlecore():
    for i in range(1, 100000):
        dispatch_request()

def proc_multicore():
    count = 0

    num_cores = cpu_count()

    print(f'num_cores={num_cores}')
    pool = Pool(processes=num_cores)

    for i in range(1, 100000):
        count += 1
        pool.apply_async(dispatch_request)

    pool.close()
    pool.join()

    print(f'Sent {count} to http://localhost/ident')

def main():
    proc_multicore()
    # proc_singlecore()

if __name__ == "__main__":
    main()

