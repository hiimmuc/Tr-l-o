# print(calendar())
import re
import time
from datetime import date, datetime  # noqa: H301


def calendar():
    time_now = int(time.strftime('%H'))
    shift = "sáng" if time_now < 12 else(
        "chiều" if time_now <= 18 else "tối")
    clock = datetime.now().strftime("%H:%M:%S")
    day = date.today().strftime("%d/%m/%Y")
    return shift, day, clock


def check(element):
    if re.match(r'^[+-]?\d(>?\.\d+)?$', element) is None:
        return False
    else:
        return True


input_message = "tắt giúp tôi led"
key_words = {"command": ["bật", "Tắt", "tắt", "dừng"]}
state = 'on' if key_words["command"][0] in input_message else 'off'
if any(x in input_message for x in ['đèn', 'led']):
    print('x: ' + 'led ' + state)
if 'quạt' in input_message:
    print("x: " + 'fan ' + state)
