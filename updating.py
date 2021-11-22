import random
import requests
import time


def trigger_update():
    try:
        requests.get('http://localhost:7898/run-test')
    except Exception:
        pass


if __name__ == '__main__':
    time.sleep(5)
    trigger_update()
    while True:
        time.sleep(random.randint(30, 10800))
        trigger_update()
