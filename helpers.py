import os
import random
import time
import webbrowser
from datetime import date, datetime

import googlesearch
import requests
import wikipedia
from arduinoConfig import ArduinoConfig
from google_trans_new import google_translator as Translator
from youtube_search import YoutubeSearch


class tools():
    def __init__(self):
        super(tools, self).__init__()
        wikipedia.set_lang('vi')
        try:
            self.com_path = 'COM6'
            self.myArduino = ArduinoConfig(self.com_path)
        except Exception:
            print('com error')
            pass

    def stop_arduino(self):
        self.myArduino.stop()

    def wait(self, t=1):
        time.sleep(t)

    def convert_languages(self, txt, src='vi', dest='en'):
        '''translating'''
        try:
            translator = Translator()
            script = translator.translate(txt, lang_src=src, lang_tgt=dest)
            return script
        except Exception:
            return ""

    def calendar(self):
        '''get the current time'''
        time_now = int(time.strftime('%H'))
        shift = "sáng" if time_now < 12 else (
            "chiều" if time_now <= 18 else "tối")
        clock = datetime.now().strftime("%H:%M:%S")
        day = date.today().strftime("%d/%m/%Y")
        return shift, day, clock

    def weather_outdoor(self, city_name):
        '''get the weather information online from accuweather api'''
        try:
            api = "330ff11e86b5ccbeba0a2f71aab88014"
            city_name = self.convert_languages(city_name, 'vi',
                                               'en').replace(' ', '').lower()
            url = f"http://api.openweathermap.org/data/2.5/weather?appid={api}&q={city_name}"
            response = requests.get(url)
            data = response.json()

            if data["cod"] != "404":
                data_table = data["main"]
                current_temperature = data_table['temp'] - 273.15
                current_pressure = data_table["pressure"]
                current_humidity = data_table["humidity"]
                some_text = data["weather"]
                weather_description = some_text[0]["description"]
                weather_description = self.convert_languages(
                    weather_description, 'en', 'vi')
                thinking = f"Hiện đang có {weather_description}, \n Nhiệt độ là {current_temperature} độ C, \n Độ ẩm là {current_humidity} %, \n Áp suất là {current_pressure} héc tơ Pascal"
        except Exception:
            thinking = "không thấy thông tin, chuyển sang dùng google"
            kw = "Thời tiết tại" + city_name
            self.gg_search(kw, max_results=1)

        return thinking

    def gg_search(self, key, max_results=5):
        '''search top 5 results with browser'''
        try:
            for i, url in enumerate(
                    googlesearch.search(key, num=max_results, stop=max_results, pause=1)):
                print(f"{i+1}-> {url}")
                webbrowser.open(str(url))
            return True
        except Exception:
            return False
        pass

    def read_news(self, what):
        '''read news abuot somthing'''
        params = {
            'apiKey': '30d02d187f7140faacf9ccd27a1441ad',
            "q": what,
        }
        api_result = requests.get('http://newsapi.org/v2/top-headlines?',
                                  params)
        api_response = api_result.json()
        print("Tin tức")

        for number, result in enumerate(api_response['articles'], start=1):
            print(
                f"""Tin {number}:\nTiêu đề: {result['title']}\nTrích dẫn: {result['description']}\nLink: {result['url']}
        """)
            if number <= 3:
                webbrowser.open(result['url'])

    def wiki(self, key_word):
        return wikipedia.summary(key_word, sentences=1)

    #  communicate with serial
    def send_command(self, command):
        # send command to control devices
        msg = "x:"
        for c in command:
            msg += (' ' + c)
        self.myArduino.send_data(msg)
        pass

    def weather_indoor(self, what):
        '''get the weather information from sensor at home'''
        info = {
            'temperature': 0,
            'humidity': 1,
            'light': 5,
            'dust': 3,
            'gas': 4,
            'rain': 2
        }
        return self.myArduino.get_data()[info[what]]
        pass

    def open_application(self, what):
        '''open application'''
        if what in ['browser', "trình duyệt", "trình tìm kiếm"]:
            path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        elif what == 'word':
            path = r"pathtoword"
        elif what == 'excel':
            path = r"pathtoword"
        os.startfile(path)
        pass

    def youtube(self, what):
        '''play youtube video'''
        while True:
            result = YoutubeSearch(what, max_results=10).to_dict()
            if result:
                break
        url = 'https://www.youtube.com' + result[0]['channel_link']
        webbrowser.open(url)

    def play_music(self, name=None, number=None):
        '''play music in pc'''
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
                self.wait(1)
                break
        pass
