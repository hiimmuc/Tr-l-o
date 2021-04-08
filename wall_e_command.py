from datetime import datetime, time
from datetime import date
import datetime
import pyowm
import googlesearch
import webbrowser
import wikipedia
from faceModule import face_detection_module
from gtts import gTTS
from playsound import playsound
import os
from mutagen.mp3 import MP3
import time


def walle_say(x):
    try:
        os.remove("Voices/voices.mp3")
    except:
        pass
    tts = gTTS(text=x, lang="vi", slow=False)
    tts.save("Voices/voices.mp3")
    voice_length = MP3("Voices/voices.mp3").info.length
    playsound("Voices/voices.mp3", True)

def walle_hello(x):
    if x == "xin chào":
        walle_say("Chào bạn! Tôi có thể giúp gì cho bạn ?")
        # walle_say('Hello ^_^')
        # voice.#voice_walle_goodbye()


def walle_boss(x):
    if "ai tạo ra" in x or "ai làm ra" in x or "chủ của bạn" in x:
        # voice.#voice_walle_tada()
        walle_say("Học sinh lớp 6 Trường THCS Chu Văn An :v :v :v  ")


def walle_intro(x):
    if "bạn là ai" in x:
        # voice.#voice_walle_name()
        walle_say("Walllllllllllll-E")


def walle_day_of_week(x):
    if "hôm nay là thứ mấy" in x:
        # voice.#voice_walle_tada()
        today = date.today()
        today = str(today)
        weekDays = ("Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật")
        today = today.split('-')
        Today = []
        for i in range(0, 3):
            Today.append(int(today[i]))
        Today_2 = datetime.date(Today[0], Today[1], Today[2]).weekday()
        Today_date = weekDays[Today_2]
        walle_say(f'Hôm nay là {Today_date}')


def walle_date(x):
    if "hôm này là ngày" in x or "ngày bao nhiêu" in x:
        now = datetime.datetime.now()
        cur_time = str(now.strftime("%d.%m.%Y"))
        today = cur_time.split(".")
        walle_say(f'Hôm nay là ngày {today[0]} tháng {today[1]} năm {today[2]} ')


def walle_kiss(x):
    if "tôi yêu bạn" in x:
        walle_say("Tôi cũng yêu bạn ")
        # voice.#voice_walle_kiss()


def walle_weather(x):
    if "thời tiết ngoài trời" in x or "thời tiết hôm nay" in x:

        # voice.#voice_walle_tada()
        owm = pyowm.OWM('29ece0bb17640e37366e161f0a24f696')

        location = owm.weather_at_place('Ha Noi, VN')
        weather = location.get_weather()
        temp = weather.get_temperature('celsius')
        humidity = weather.get_humidity()

        status = weather.get_status()
        walle_say(f"Trạng thái thời tiết là {status}")
        #
        # walle_say(weather)
        for key, value in temp.items():
            walle_say("Nhiệt độ ngoài trời là")
            walle_say(f"{value}")
            break

        walle_say(f"Độ ẩm ngoài trời là {humidity}")
    elif "nhiệt độ ngoài trời" in x or "nhiệt độ hiện tại" in x:
        owm = pyowm.OWM('29ece0bb17640e37366e161f0a24f696')

        location = owm.weather_at_place('Ha Noi, VN')
        weather = location.get_weather()
        temp = weather.get_temperature('celsius')

        for key, value in temp.items():
            walle_say("Nhiệt độ ngoài trời là")
            walle_say(f"{value}")
            break

    elif "độ ẩm ngoài trời" in x or "độ ẩm hiện tại" in x:
        # voice.#voice_walle_tada()
        owm = pyowm.OWM('29ece0bb17640e37366e161f0a24f696')

        location = owm.weather_at_place('Ha Noi, VN')
        weather = location.get_weather()
        humidity = weather.get_humidity()

        walle_say(f"Độ ẩm: {humidity}")


def walle_go_to_sleep(x):
    if "tạm biệt" in x or "tôi hài lòng" in x or "kết thúc làm việc" in x:
        # voice.#voice_walle_goodbye()
        walle_say("Tạm biệt !")


def walle_time(x):
    if "mấy giờ rồi" in x or "bây giờ là mấy giờ" in x:
        now = datetime.datetime.now()
        cur_time = str(now.strftime("%H:%M:%S"))
        cur_time = cur_time.split(":")
        walle_say(f"Bây giờ là {cur_time[0]} giờ {cur_time[1]} phút {cur_time[2]} giây")


def walle_search(x):
    if ("tìm kiếm" in x or "search" in x) and "wiki" not in x and ("đóng" not in x or "tắt" not in x):
        stop_word = ["tìm kiếm", "search", "wiki"]
        for word in stop_word:
            if word in x:
                x.replace(word, "")
        try:
            result = googlesearch.search(x)
            webbrowser.register('chrome',
                                None,
                                webbrowser.BackgroundBrowser(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"))
            if len(result) > 0:
                webbrowser.get("chrome").open(str(result[0]))
            walle_say(f"Tôi tìm được trang này!")
        except:
            walle_say("Không tìm được")

def walle_close_search(x):
    if "đóng tìm kiếm" in x or "tắt trang" in x or "đóng trang" in x:
        # webbrowser_name = "launcher.exe"
        os.system("taskkill /im chrome.exe /f")
        walle_say("Đã đóng cửa sổ tìm kiếm !")

def walle_wiki(x):
    if "wiki" in x:
        stop_word = ["tìm kiếm", "search", "wiki"]
        for word in stop_word:
            if word in x:
                x.replace(word, "")
        # walle_say(wikipedia.search(x))
        # walle_say(wikipedia.summary(x, sentences=1))
        print("Tôi tìm được trang này !")
def walle_arduino(x):
    if "nhà thông minh" in x:
        walle_say("Đã chuyển sang chế độ nhà thông minh !")
        return True

def walle_arduino_mode(x):
    if "thủ công" in x:
        walle_say("Chế độ thủ công ")
    else:
        walle_say("Chế độ tự động ")

def walle_arduino_command(x):
    if "tắt đèn" in x:
        walle_say("Đã tắt đèn")
        return "x: ledoff\n"
    elif "bật đèn" in x or "mở đèn" in x:
        walle_say("Đã bật đèn")
        return "x: ledon\n"
    elif "tắt quạt" in x:
        walle_say("Đã tắt quạt")
        return "x: quatoff\n"
    elif "bật quạt" in x or "mở quạt" in x:
        walle_say("Đã bật quạt")
        return "x: quaton\n"
    elif "bật cảnh báo" in x:
        walle_say("Đã bật cảnh báo")
        return "x: warning\n"
    elif "tắt cảnh báo" in x or "đóng cảnh báo" in x:
        walle_say("Đã tắt cảnh báo")
        return "x: nowarning\n"
    else:
        return None

def walle_face_register(x):
    if "đăng ký khuôn mặt" in x or "thêm khuôn mặt" in x or "đăng ký khuôn mập" in x or "thêm khuôn mập" in x:
        name = str(input("Nhập vào tên đăng ký, viết không dấu (Nhập cancle nếu muốn hủy):"))
        if name == 'cancel':
            return
        if name in os.listdir("Dataset/boss"):
            walle_say("Tên đã được sử dụng !")
        else:
            walle_say("Băt đầu đăng ký khuôn mặt! Hãy nhìn vào camera vào xoay đầu nhẹ sang các hướng ! ")
            face_detection_module.face_register(name)
            face_detection_module.encode_pickle()
            walle_say("Đã xong !")


def walle_scan_face(x):
    if "quét mặt" in x or "quét khuôn mặt" in x or "scan" in x or "quét mập" in x:
        if not os.listdir("Dataset/boss"):
            walle_say("Chưa có khuôn mặt nào được đăng ký !")
            return True
        owner, name = face_detection_module.face_check()
        if owner:
            walle_say(f"Chào mừng {name}")
        else:
            walle_say("Không xác định !")
        return owner

def walle_delete_face(x):
    if "xóa mặt" in x or "xóa khuôn mặt" in x or "xóa mập" in x or "xóa khuôn mập" in x:
        nameList = os.listdir("Dataset/boss")
        if not nameList:
            walle_say("Không có khuôn mặt nào trong database !")
            return
        print("Danh sách khuôn mặt đã đăng ký: \n")
        for i, name in enumerate(nameList):
            print(f"{i+1} - {name}")
        delName = str(input("Bạn muốn xóa tên nào (Nhập số thứ tự hoặc nhập tên, nhập cancle để hủy):"))
        while "cancel" not in delName:
            if delName.isnumeric():
                delName = int(delName)
                if delName > len(nameList) or delName <= 0:
                    delName = str(input("Không có số thứ tự trong đó ! Mời nhập lại: "))
                else:
                    for rm in os.listdir(f"Dataset/boss/{nameList[delName - 1]}"):
                        os.remove(f"Dataset/boss/{nameList[delName - 1]}/{rm}")
                    time.sleep(1)
                    os.rmdir(f"Dataset/boss/{nameList[delName - 1]}")
                    os.remove(f"Dataset/pickleFile/{nameList[delName - 1]}.pkl")
                    walle_say("Đã xóa mặt")
                    return
            else:
                if delName not in nameList:
                    delName = str(input("Không có tên trong đó ! Mời nhập lại: "))
                else:
                    for rm in os.listdir(f"Dataset/boss/{delName}"):
                        os.remove(f"Dataset/boss/{delName}/{rm}")
                    time.sleep(1)
                    os.rmdir(f"Dataset/boss/{delName}")
                    os.remove(f"Dataset/pickleFile/{delName}.pkl")
                    walle_say("Đã xóa mặt !")
                    return
        else:
            walle_say("Đã hủy")
            return

def check_in_house(x):
    listCheck = ["nhiệt độ trong phòng", "độ ẩm trong phòng", "cường độ ánh sáng", "độ bụi", "khí ga", "khí gas", "mưa"]
    for check in listCheck:
        if check in x:
            return True
    return False

def walle_all_command(x):
    walle_go_to_sleep(x)
    walle_hello(x)
    walle_weather(x)
    walle_intro(x)
    walle_day_of_week(x)
    walle_kiss(x)
    walle_date(x)
    walle_boss(x)
    walle_search(x)
    walle_close_search(x)
    walle_wiki(x)
    walle_time(x)





