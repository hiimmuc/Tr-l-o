# from gtts import gTTS
import os
import random
import time
from datetime import date, datetime  # noqa: H301

import pyttsx3
import requests
import speech_recognition
import wikipedia
from google_trans_new import google_translator as Translator  # noqa: H306
from googlesearch import search
from requests.api import get  # noqa: F401

path = r"F:\Tài Liệu Học\Machine Learning\code"
path = os.path.join(path, "audio.mp3")

data = {
    "research": ["tìm thông tin", "hỏi"],
    "search": ["tìm kiếm", "kiểm tra", "google", "gu gồ", "tra cứu",
               "tra"],  # noqa: E501
    "check": ["ngày", "giờ", "thời tiết"],
    "greet": ["xin chào", "hello", "hi", "hai"],
    "action": ["play music", "chơi nhạc", "nhạc", "trình duyệt"],
    "bye": ["kết thúc", "tạm biệt", "hẹn gặp lại"]
}
running = True
robot_speak = pyttsx3.init()
robot_ear = speech_recognition.Recognizer()


def get_text(low=True):
    input_message = ""
    thinking = ""
    understand = True
    with speech_recognition.Microphone() as mic:
        print("Ready!")
        robot_ear.adjust_for_ambient_noise(mic)
        audio = robot_ear.record(mic, duration=3)  # listen in 3 seconds
    try:
        print("You: ", end='')
        input_message = robot_ear.recognize_google(audio, language='vi-VN')
        print(input_message)
        understand = True
    except Exception:  # noqa: E722
        thinking = "Tôi không hiểu bạn nói gì cả ! ..."
        understand = False
    input_message = input_message if not low else input_message.lower()
    return (input_message,
            understand) if understand else (thinking, understand)  # noqa: E501


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
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={api}&q={city_name}"  # noqa: E501
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


def robot_say(thinking):
    thinking = convert_languages(thinking, 'vi', 'en')
    robot_speak.say(thinking)
    robot_speak.runAndWait()


def browser():
    browser_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    os.startfile(browser_path)
    pass


def wait(t=1):
    time.sleep(t)


robot_say("Hello, my name is Friday, can i help u?")

while running:
    # khởi tạo
    thinking = "..."
    input_message = ""  # chua noi gi
    robot_say("I'm listening")
    print("\nFriday: I'm listening....")
    input_message, some_text = get_text()
    input_message = input_message if some_text else thinking
    for key in data:
        if any(text in input_message for text in data[key]):
            if key == "greet":
                thinking = "Hi there"
            elif key == "action":
                if data[key][-1] in input_message:
                    browser()
                else:
                    play_music()
                pass
            elif key == "check":
                if data[key][0] in input_message:
                    thinking = date.today().strftime("%d/%m/%Y")
                elif data[key][1] in input_message:
                    thinking = datetime.now().strftime("%H:%M:%S")
                elif data[key][2] in input_message:
                    print("\nFriday: Tên thành phố cần tìm...")
                    robot_say("Tên thành phố cần tìm")
                    city, _ = get_text(False)
                    thinking = weather(city_name=city)
            elif key == "search":
                print("\nFriday: " + "Bạn muốn tìm gì")
                robot_say("Bạn muốn tìm gì")
                key, _ = get_text()
                if gg_search(key):
                    thinking = "tôi tìm thấy cái này"
                else:
                    thinking = "tôi không thấy gì vè nó cả"
                pass
            elif key == "research":
                print("\nFriday: " + "Bạn muốn gì")
                robot_say("Bạn muốn gì")
                key_word, _ = get_text()
                try:
                    thinking = wikipedia.summary(key_word, sentences=1)
                except Exception:
                    thinking = "tôi không thấy gì"
            else:
                break

    if any(text in input_message for text in data["bye"]) or not running:
        thinking = "cảm ơn bạn, tạm biệt"
        running = False

    print(f"\nFriday: {thinking}")
    robot_say(thinking=thinking)
    # tts = gTTS(text=thinking, lang='vi')
    # tts.save(path)
    # os.system("start audio.mp3")
