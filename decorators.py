# დეკორატორები: დროის გაზომვა და ხელახლა ცდა
import time
from functools import wraps

import requests


def timer(func):
    # ზომავს, რამდენ ხანს მუშაობდა ფუნქცია
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"\n(დრო: {time.time() - start:.2f} წამი)")
        return result
    return wrapper


def retry(times=3, delay=1):
    # თუ ინტერნეტის პრობლემის გამო ჩავარდა, რამდენჯერმე ვცდით თავიდან
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                    if attempt == times:
                        raise
                    print(f"კავშირი ვერ მოხერხდა, ვცდი თავიდან ({attempt}/{times})...")
                    time.sleep(delay)
        return wrapper
    return decorator