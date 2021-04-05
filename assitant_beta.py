import os
import time
from datetime import date, datetime

import helpers
import playsound
import pyttsx3
import speech_recognition
from gtts import gTTS
from KW import readJson as QA


class MyAssistant():
    def __init__(self):
        super(MyAssistant, self).__init__()
        self.language = 'vi'
        self.running = True
        self.speaker = pyttsx3.init()
        self.recorder = speech_recognition.Recognizer()
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

            if any(text in input_message
                   for text in self.keywords["bye"]) or not self.running:
                thinking = "Cảm ơn bạn, tạm biệt"
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
        thinking = text if text != '...' else "tôi chưa hiểu, vui lòng nói lại"
        try:
            self.tts = gTTS(text=thinking, lang='vi', slow=False)
            self.tts.save("backup/voices.mp3")
            playsound.playsound("backup/voices.mp3", False)
            os.remove("backup/voices.mp3")
            helpers.wait(t=2)
        except Exception:
            print("switch mode to english")
            thinking = helpers.convert_languages(
                text, 'vi', 'en') if lang == 'en' else text
            if lang == 'en':
                self.speaker.say(thinking)
                self.speaker.runAndWait()
        pass
