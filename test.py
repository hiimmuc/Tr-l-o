
import re
import time
from datetime import date, datetime

from google_trans_new import google_translator as Translator
from helpers import tools


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


mytools = tools()
translator = Translator()
input_message = "thời tiết ở Hà Nội"
kw = input_message[input_message.rfind('ở') + len('ở'):]
script = translator.translate(kw, lang_src='vi', lang_tgt='en')
print(script)
print(mytools.weather_outdoor(script))
