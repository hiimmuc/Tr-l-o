import os
import random

import playsound
import pyttsx3
import speech_recognition
from gtts import gTTS
from helpers import tools
from mutagen.mp3 import MP3


class MyAssistant():
    def __init__(self):
        super(MyAssistant, self).__init__()
        self.helpers = tools()
        self.language = 'vi'
        self.running = True
        self.speaker = pyttsx3.init()
        self.recorder = speech_recognition.Recognizer()
        self.keywords = {
            "info": ["nhiệt độ", "độ ẩm", "lượng mưa", "ánh sáng", "bụi", "khí ga"],
            "research": ["tìm thông tin", "hỏi"],
            "search":
            ["tìm kiếm", "kiểm tra", "google", "gu gồ", "tra cứu", "tra"],
            "check": ["ngày bao nhiêu", "mấy giờ", "thời tiết"],
            "greet": ["xin chào", "hello"],
            "open": ["play music", "chơi nhạc", "nhạc", "trình duyệt", "youtube"],
            "bye": ["kết thúc", "tạm biệt", "hẹn gặp lại"],
            "news": ["báo"],
            "command": ["bật", "Tắt", "tắt", "dừng"]
        }
        self.aspect = {
            "nhiệt độ": 'temperature',
            "độ ẩm": 'humidity',
            "lượng mưa": 'rain',
            "ánh sáng": 'light',
            "bụi": 'dust',
            "khí ga": "gas",
        }
        pass

    def run(self):
        print("Xin chào, tôi là Friday, tôi có thể giúp gì?")
        self.speak("Xin chào, tôi là Friday, tôi có thể giúp gì?")
        while self.running:
            # khởi tạo
            thinking = "..."
            input_message = ""
            print("\nFriday: Tôi đang nghe ...")
            self.speak("Tôi đang nghe")
            input_message, understand = self.listen()
            if understand:
                for key in self.keywords:
                    if any(text in input_message for text in self.keywords[key]):
                        if key == "greet":
                            calendar_now = self.helpers.calendar()
                            shift = calendar_now[0]
                            thinking = random.choice(
                                ["Chào bạn", "xin chào", "Chào buổi " + shift])
                        elif key == "open":
                            if self.keywords[key][-1] in input_message:
                                self.helpers.open_application('browser')
                            elif self.keywords[key][-2] in input_message:
                                what = self.get_target(input_message, key)
                                self.helpers.youtube(what)
                            else:
                                self.helpers.play_music()
                        elif key == "check":
                            calendar_now = self.helpers.calendar()
                            if self.keywords[key][0] in input_message:
                                thinking = calendar_now[1]
                            elif self.keywords[key][1] in input_message:
                                thinking = calendar_now[2]
                            elif self.keywords[key][2] in input_message:
                                city = self.get_target(input_message, key)
                                thinking = self.helpers.weather_outdoor(
                                    city_name=city)
                        elif key == "search":
                            kw = self.get_target(input_message, key)
                            if self.helpers.gg_search(kw):
                                thinking = "tôi tìm thấy cái này"
                            else:
                                thinking = "tôi không thấy gì vè nó cả"
                            pass
                        elif key == "research":
                            key_word = self.get_target(input_message, key)
                            try:
                                thinking = self.helpers.wiki(key_word)
                            except Exception:
                                thinking = "tôi không thấy gì"
                        elif key == "news":
                            about = self.get_target(input_message, key)
                            self.helpers.read_news(about)
                        elif key == "info":
                            for about in self.keywords["info"]:
                                if about in input_message:
                                    try:
                                        what = self.aspect[about]
                                    except Exception:
                                        what = ""
                                    value = self.helpers.weather_indoor(what)
                                    thinking = about + " hiện giờ là " + str(value)

                        elif key == 'command':
                            state = 'on' if self.keywords[key][
                                0] in input_message else 'off'
                            if 'đèn' in input_message:
                                self.helpers.send_command(['led', state])
                            if 'quạt' in input_message:
                                self.helpers.send_command(['fan', state])
                            pass
                        else:
                            continue

                if any(text in input_message
                       for text in self.keywords["bye"]) or not self.running:
                    thinking = "cảm ơn bạn, tạm biệt"
                    self.running = False
            else:
                thinking = "tôi không hiểu ý bạn, hãy thử nói lại lần nữa"
            thinking = thinking if thinking != '...' else "tôi không nghe rõ, vui lòng nói lại"
            print(f"\nFriday: {thinking}")
            self.speak(text=thinking)
        pass

    def get_target(self, input_message, catergory):
        '''get the target name, it usually go with o, tai, ve,..'''
        got_it = False
        kw = ""
        if catergory == 'check':
            signs = ['ở', 'tại']
            for sign in signs:
                if sign in input_message:
                    kw = input_message[input_message.rfind(sign) + len(sign):]
                    kw = self.helpers.convert_languages(kw)
                    if kw.strip() == '':
                        print("\nFriday: Tên thành phố cần tìm...")
                        self.speak("Tên thành phố cần tìm")
                        kw, _ = self.listen(False)
        if catergory in ['search', 'research', 'news', 'open']:
            if "về" in input_message:
                kw = input_message[input_message.rfind("về") + 2:]
                if kw.strip() != '':
                    got_it = True
            elif ("về" not in input_message) or (not got_it):
                print("\nFriday: " + "Bạn muốn tìm gì")
                self.speak("Bạn muốn tìm gì")
                kw, _ = self.listen()
        return kw

    def listen(self, lowercase=True):
        ''''''
        input_message = ""
        thinking = "..."
        understand = True
        with speech_recognition.Microphone() as mic:
            print("You:", end='')
            self.recorder.adjust_for_ambient_noise(mic)
            print("->> ", end='')
            audio = self.recorder.listen(mic, phrase_time_limit=4)
        try:
            input_message = self.recorder.recognize_google(audio,
                                                           language='vi-VN')
            print(input_message)
            understand = True
        except Exception:
            understand = False
        input_message = input_message if not lowercase else input_message.lower(
        )
        return (input_message, understand) if understand else (thinking,
                                                               understand)
        pass

    def speak(self, text, lang='vi'):
        try:
            self.tts = gTTS(text=thinking, lang=lang, slow=False)
            self.tts.save("backup/voices.mp3")
            voice_length = MP3("backup/voices.mp3").info.length
            playsound.playsound("backup/voices.mp3", False)
            self.helpers.wait(t=(voice_length + 0.5))
            os.remove("backup/voices.mp3")

        except Exception:
            print("switch mode to english")
            thinking = self.helpers.convert_languages(text, 'vi', 'en')
            self.speaker.say(thinking)
            self.speaker.runAndWait()
        pass

    def stop(self):
        self.running = False


friday = MyAssistant()
friday.run()
