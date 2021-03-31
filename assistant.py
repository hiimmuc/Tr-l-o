import time
from datetime import date, datetime

import helpers
import pyttsx3
import speech_recognition


class MyAssistant():
    def __init__(self):
        super(MyAssistant, self).__init__()
        self.running = True
        self.speaker = pyttsx3.init()
        self.recorder = speech_recognition.Recognizer()
        self.keywords = {
            "info": ["nhiệt độ", "độ ẩm", "mưa"],
            "research": ["tìm thông tin", "hỏi"],
            "search":
            ["tìm kiếm", "kiểm tra", "google", "gu gồ", "tra cứu", "tra"],
            "check": ["ngày", "giờ", "thời tiết"],
            "greet": ["xin chào", "hello", "hi", "hai"],
            "action": ["play music", "chơi nhạc", "nhạc", "trình duyệt"],
            "bye": ["kết thúc", "tạm biệt", "hẹn gặp lại"],
            "command": ["bật", "Tắt", "tắt", "dừng"]
        }
        pass

    def run(self):
        self.speak("Hello, my name is Friday, can i help u?")
        while self.running:
            # khởi tạo
            thinking = "..."
            input_message = ""  # chua noi gi
            self.speak("I'm listening")
            print("\nFriday: I'm listening....")
            input_message, understand = self.listen()
            input_message = input_message.lower() if understand else thinking
            for key in self.keywords:
                if any(text in input_message for text in self.keywords[key]):
                    if key == "greet":
                        thinking = "Hi there"
                    elif key == "action":
                        pass
                    elif key == "check":
                        if self.keywords[key][0] in input_message:
                            thinking = date.today().strftime("%d/%m/%Y")
                        elif self.keywords[key][1] in input_message:
                            thinking = datetime.now().strftime("%H:%M:%S")
                        elif self.keywords[key][2] in input_message:
                            print("\nFriday: Tên thành phố cần tìm...")
                            self.speak("Tên thành phố cần tìm")
                            city, _ = self.listen(False)
                            thinking = helpers.weather(city_name=city)
                    elif key == "search":
                        print("\nFriday: " + "Bạn muốn tìm gì")
                        self.speak("Bạn muốn tìm gì")
                        key, _ = self.listen()
                        if helpers.gg_search(key):
                            thinking = "tôi tìm thấy cái này"
                        else:
                            thinking = "tôi không thấy gì vè nó cả"
                        pass
                    elif key == "research":
                        print("\nFriday: " + "Bạn muốn gì")
                        self.speak("Bạn muốn gì")
                        key_word, _ = self.listen()
                        try:
                            thinking = helpers.wiki(key_word)
                        except Exception:
                            thinking = "tôi không thấy gì"
                    elif key == "command":
                        if self.keywords[key][0] in input_message:
                            helpers.send_command(('output', 'led', 0.2),
                                                 'port')
                        if self.keywords[key][1] in input_message:
                            helpers.send_command(('output', 'led', 0.0),
                                                 'port')
                    else:
                        break

            if any(text in input_message
                   for text in self.keywords["bye"]) or not self.running:
                thinking = "cảm ơn bạn, tạm biệt"
                self.running = False

            print(f"\nFriday: {thinking}")
            self.speak(text=thinking)
        pass

    def listen(self, lowercase=True):
        input_message = ""
        thinking = ""
        understand = True
        with speech_recognition.Microphone() as mic:

            self.recorder.adjust_for_ambient_noise(mic)
            audio = self.recorder.record(mic,
                                         duration=3)  # listen in 3 seconds
            print("Ready!")
        try:
            print("You: ", end='')
            input_message = self.recorder.recognize_google(audio,
                                                           language='vi-VN')
            print(input_message)
            understand = True
        except Exception:  # noqa: E722
            thinking = "Tôi không hiểu bạn nói gì cả ! ..."
            understand = False
        input_message = input_message if not lowercase else input_message.lower(
        )
        return (input_message, understand) if understand else (thinking,
                                                               understand)
        pass

    def speak(self, text):
        thinking = helpers.convert_languages(text, 'vi', 'en')
        self.speaker.say(thinking)
        self.speaker.runAndWait()
        pass
