import speech_recognition
import playsound
# from voice import voice_path


def walle_listen():
    robot_ear = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as mic:
        robot_ear.adjust_for_ambient_noise(mic)
        print("I'm listening")
        audio = robot_ear.record(mic,duration=5)
    try:
        answer =robot_ear.recognize_google(audio, language='vi')
    except:
        answer = ""
    return answer



