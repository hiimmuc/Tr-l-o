import os
import random
import time
from datetime import date, datetime  # noqa: H301

import requests
import speech_recognition
import wikipedia
from arduinoConfig import ArduinoConfig
from google_trans_new import google_translator as Translator  # noqa: H306
from googlesearch import search
from requests.api import get

com_path = 'COM6'
myArduino = ArduinoConfig(com_path)


def play_music(name=None, number=None):
    music_path = r"F:\Musics\US-UK"
    songs = os.listdir(music_path)
    if not name and not number:
        k = random.randint(0, len(songs) - 1)
        print(f"Playing {songs[k]}", end="...\n")
        os.startfile(os.path.join(music_path, songs[k]))
    else:
        if name:
            for x in songs:
                if name.lower() in x.lower():
                    print(f"Playing {x}...")
                    os.startfile(os.path.join(music_path, x))
                    break
            else:
                print("the song is not valid")
        elif number and number < len(songs):
            print(f"Playing {songs[number]}...")
            os.startfile(os.path.join(music_path, songs[number]))

    while True:
        if str(input("Pause?: (Y/N): ")).lower() == 'y':
            os.system("TASKKILL /F /IM Music.UI.exe")
            wait(1)
            break
    pass


def convert_languages(txt, src='vi', dest='en'):
    try:
        translator = Translator()
        script = translator.translate(txt, lang_src=src, lang_tgt=dest)
        return script
    except Exception:  # noqa: E722, H201
        return ""


def weather(city_name):
    api = "330ff11e86b5ccbeba0a2f71aab88014"
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={api}&q={city_name}"
    response = requests.get(url)
    data = response.json()
    city_name = convert_languages(city_name, 'vi', 'en').replace(' ',
                                                                 '').lower()
    if data["cod"] != "404":
        data_table = data["main"]
        current_temperature = f"{data_table['temp'] - 273.15} Celcius degree"
        current_pressure = data_table["pressure"]
        current_humidity = data_table["humidity"]
        some_text = data["weather"]
        weather_description = some_text[0]["description"]
        weather_description = convert_languages(weather_description, 'en',
                                                'vi')
        thinking = f"Hiện đang có {weather_description}, \n\
        Nhiệt độ là {current_temperature}, \n\
        Độ ẩm là {current_humidity}, \n\
        áp suất là {current_pressure}"

    else:
        thinking = "không thấy thông tin"
    return thinking


def gg_search(key):
    try:
        for i, url in enumerate(search(key, num=15, stop=15, pause=1)):
            print(f"{i+1}-> {url}")
        return True
    except Exception:  # noqa: E722
        return False
    pass


def browser():
    browser_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    os.startfile(browser_path)
    pass


def wait(t=1):
    time.sleep(t)


def wiki(key_word):
    return wikipedia.summary(key_word, sentences=1)


def send_command(command, how):
    _, tp, value = command
    if how.lower() == 'terminal':
        myArduino.transfer_data_terminal(tp, value)
    elif how.lower() == "port":
        myArduino.transfer_data_port(tp, value)
    print("done sending")


def get_information(about, how):

    if how.lower() == 'terminal':
        myArduino.get_data_terminal()
    elif how.lower() == "port":
        myArduino.get_data_port(about)
    print("done sending")
