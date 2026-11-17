# დეკორატორები: დროის გაზომვა და ხელახლა ცდა
# დეკორატორი ფუნქციის კოდს არ ცვლის, უბრალოდ "გარშემო" ამატებს დამატებით ქცევას
import time
from functools import wraps

import requests


# timer - ზომავს, რამდენ ხანს მუშაობდა ფუნქცია
def timer(func):
    # @wraps - ფუნქციას თავისი სახელი და აღწერა რჩება (wrapper-ად არ იქცევა)
    @wraps(func)
    # *args, **kwargs - ნებისმიერი პარამეტრები მიიღოს და ორიგინალ ფუნქციას გადასცეს
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        # :.2f - დრო 2 ციფრით წერტილის შემდეგ
        print(f"\n(დრო: {time.time() - start:.2f} წამი)")
        return result
    return wrapper


# retry - თუ ინტერნეტის პრობლემის გამო ჩავარდა, რამდენჯერმე ცდის თავიდან
# პარამეტრები აქვს (times, delay), ამიტომ ერთი დონე მეტია: retry -> decorator -> wrapper
def retry(times=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                # თუ ფუნქციამ იმუშავა, შედეგი მაშინვე ბრუნდება და ციკლი მთავრდება
                try:
                    return func(*args, **kwargs)
                # მხოლოდ კავშირის შეცდომებზე ცდის თავიდან. KeyError-ზე (ქალაქი ვერ მოიძებნა) აზრი არ აქვს
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                    # ბოლო მცდელობაც თუ ჩავარდა, raise იმავე შეცდომას ისვრის და main.py-ში დაიჭირება
                    if attempt == times:
                        raise
                    print(f"კავშირი ვერ მოხერხდა, ვცდი თავიდან ({attempt}/{times})...")
                    # ახალ მცდელობამდე delay წამი ლოდინი
                    time.sleep(delay)
        return wrapper
    return decorator
