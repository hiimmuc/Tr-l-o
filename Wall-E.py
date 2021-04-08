import pyttsx3
import time
import listen
import wall_e_command
from wall_e_command import *
import serial

arduino_fine = True
com_path = "COM9"
try:
    ser = serial.Serial(com_path, 9600)
    print("Connected to Arduino !")
except:
    print("Can not connect to Arduino, please check your arduino !")
    arduino_fine = False

wake_word = False
manual = False
data = ''
owner = False
walle_hear = ''
first_voices = True
while True:
    while 'siri' not in walle_hear.lower().split(" ") and wake_word == False:
        walle_hear = listen.walle_listen()
        # walle_hear = str(input("Wake_word:"))
        print(walle_hear)
    else:
        # try:
        wake_word = True
        print("\nPlease command: ")
        if first_voices:
            walle_say("Đã kích hoạt trợ lý ảo")
            first_voices = False
        walle_hear = listen.walle_listen().lower()
        # walle_hear = str(input("input:")).lower()
        print("Walle hear: ", walle_hear)
        wall_e_command.walle_all_command(walle_hear)
        if "quét mặt" in walle_hear or "quét khuôn mặt" in walle_hear or "scan" in walle_hear:
            owner = walle_scan_face(walle_hear)
        if owner:
            walle_face_register(walle_hear)
            walle_delete_face(walle_hear)
        if owner and arduino_fine:
            if "thủ công" in walle_hear:
                walle_say("Chế độ thủ công")
                manual = True
                ser.write(bytearray("x: manual\n", "utf-8"))
                while True:
                    data_byte = ser.readline()
                    data += data_byte.decode("utf-8")
                    if walle_hear == '' or "*" in data or data == '':
                        print(data.split("------")[1])
                        data = ''
                        break
                print("Chế độ thủ công !")
            elif "auto" in walle_hear or "tự động" in walle_hear or "kết thúc" in walle_hear:
                walle_say("Chế độ auto")
                manual = False
                ser.write(bytearray("x: end\n", "utf-8"))
                while True:
                    data_byte = ser.readline()
                    data += data_byte.decode("utf-8")
                    if walle_hear == '' or "#" in data or data == '':
                        data = ''
                        break
                print("Chế độ tự động !")

            if manual and walle_hear:
                command = walle_arduino_command(walle_hear)
                check = check_in_house(walle_hear)
                if check:
                    ser.write(bytearray("x: get\n", "utf-8"))
                    while True:
                        data_byte = ser.readline()
                        data += data_byte.decode("utf-8")
                        if walle_hear == '' or "*" in data or data == '':
                            data_split = data.split("\n")
                            ii = 0
                            for i, _ in data_split:
                                if "y:" in data_split[i]:
                                    ii = i
                                    break
                            try:
                                float(data_split[ii + 1])
                                data_house = data_split[ii].split(" ")[1:6] + [data_split[ii+1]]
                            except:
                                data_house = data_split[ii].split(" ")[1:7]
                            print(data.split("\n"))
                            print(data_house)
                            data = ''
                            break
                    for i in range(len(data_house)):
                        if data_house[i] == 'nan' and i != 2:
                            data_house[i] = "Không đọc được cảm biến"
                    if "nhiệt độ" in walle_hear and ("trong phòng" in walle_hear or "trong nhà" in walle_hear):
                        walle_say(f"Nhiệt độ trong phòng là {data_house[0]}")
                    if "độ ẩm" in walle_hear and ("trong phòng" in walle_hear or "trong nhà" in walle_hear):
                        walle_say(f"Độ ẩm trong nhà là {data_house[1]}")
                    if "cường độ ánh sáng" in walle_hear:
                        walle_say(f"Cường độ ánh sáng trong nhà là {data_house[5]}")
                    if "mưa" in walle_hear:
                        if data_house[2] == 'nan':
                            walle_say("Không đọc được cảm biến ")
                        elif data_house[2] == '1':
                            walle_say("Trời đang mưa")
                        else:
                            walle_say("Trời không mưa")
                    if "khí ga" in walle_hear or "khí gas" in walle_hear:
                        walle_say(f"Nồng độ khí ga hiện tại là {data_house[4]}")
                    elif "bụi" in walle_hear:
                        walle_say(f"Mật độ bụi hiện tại là {data_house[3]}")
                if not command:
                    continue
                print("Sending")
                ser.write(bytearray(command, "utf-8"))
                while True:
                    data_byte = ser.readline()
                    data += data_byte.decode("utf-8")
                    if walle_hear == '' or "*" in data or data == '':
                        print(data)
                        data = ''
                        break
        # except:
        #     print("Không thực hiện được lệnh !")
        if "tạm biệt" in walle_hear:
            wake_word = False
            owner = False
            first_voices = True
            continue

