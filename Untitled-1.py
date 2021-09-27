import requests
import threading
from functools import lru_cache

@lru_cache
def request():
    while True:
        try:
            requests.get("https://www.google.com")
            print("Requested google")
        except ConnectionError:
            requests.get("https://www.youtube.com")
            print("Requested youtube")

def main():
    t1 = threading.Thread(target=request)
    t2 = threading.Thread(target=request)
    t3 = threading.Thread(target=request)
    t4 = threading.Thread(target=request)
    t5 = threading.Thread(target=request)
    t6 = threading.Thread(target=request)
    t7 = threading.Thread(target=request)
    t8 = threading.Thread(target=request)
    t9 = threading.Thread(target=request)
    t10 = threading.Thread(target=request)
    t11 = threading.Thread(target=request)
    t12 = threading.Thread(target=request)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()

if __name__ == '__main__':
    main()
