import os
import time
from datetime import date, datetime

import playsound
import processData as prs
import pyttsx3
import speech_recognition
from gtts import gTTS
from helpers import tools
from KW import readJson as QA


class MyAssistant():
    def __init__(self):
        super(MyAssistant, self).__init__()
        self.language = 'vi'
        self.running = True
        self.speaker = pyttsx3.init()
        self.recorder = speech_recognition.Recognizer()
        self.tools = tools()
        # self.functions = {'question': {'infor': {'status':self.tools.w}}}
        pass

    def run(self):
        self.speak("Hello, my name is Friday, can i help u?")
        self.help()
        while self.running:
            # khởi tạo
            thinking = "..."
            input_message = ""  # chua noi gi
            self.speak("I'm listening")
            print("\nFriday: I'm listening....")
            input_message, understand = self.listen()
            input_message = input_message.lower() if understand else thinking

            text_type, tag, base_answer = QA.readjson.check_text(input_message)
            data = prs.process_data(text_type, tag)
            thinking = QA.make_answer(input_message, data)

            print(f"\nFriday: {thinking}")
            self.speak(text=thinking)
        pass

    def listen(self, lowercase=True):
        ''''''
        input_message = ""
        thinking = ""
        understand = True
        with speech_recognition.Microphone() as mic:
            self.recorder.adjust_for_ambient_noise(mic)
            print("Ready!")
            audio = self.recorder.listen(mic, phrase_time_limit=3)

        try:
            print("You: ", end='')
            input_message = self.recorder.recognize_google(audio,
                                                           language='vi-VN')
            print(input_message)
            understand = True
        except Exception:
            thinking = "Tôi không hiểu bạn nói gì cả ! ..."
            understand = False
        input_message = input_message if not lowercase else input_message.lower(
        )
        return (input_message, understand) if understand else (thinking,
                                                               understand)
        pass

    def speak(self, text, lang='vi'):
        thinking = text if text != '...' else "tôi chưa nghe được, vui lòng nói lại"
        try:
            self.tts = gTTS(text=thinking, lang=lang, slow=False)
            self.tts.save("backup/voices.mp3")
            voice_length = MP3("backup/voices.mp3").info.length
            playsound.playsound("backup/voices.mp3", False)
            helpers.wait(t=(voice_length + 0.5))
            os.remove("backup/voices.mp3")

        except Exception:
            print("switch mode to english")
            thinking = helpers.convert_languages(
                text, 'vi', 'en')
            self.speaker.say(thinking)
            self.speaker.runAndWait()
        pass

    def help(self):
        self.speak("""Các chức năng cơ bản:
            1. Chào hỏi
            2. Xem ngày giờ
            3. xem thời tiết. nhiệt độ
            4. Mở website, ứng dụng
            5. Tìm kiếm trên Google, Wiki
            6. Mở nhạc
            7. Đọc báo hôm nay
            8. bật tắt, tăng giảm ánh sáng, quạt""")
