import time

import serial


class ArduinoConfig():
    def __init__(self, com):
        super(ArduinoConfig, self).__init__()
        self.com = com
        self.available = True
        self.msg = "x: get\n"
        try:
            self.terminal = serial.Serial(self.com, baudrate=9600)
        except Exception:
            try:
                print("[W] serial have been opened in another app, try to restart...")
                self.terminal.close()
                self.terminal.open()
                print("[I] done restarting")
            except Exception:
                print("[E] can not restart serial, please close all relating app")
                self.available = False

    def get_data(self):
        '''send signal to arduino and get the line of value'''
        def is_float(x):
            try:
                float(x)
                return True
            except ValueError:
                return False
        if self.available:
            self.send_data(self.msg)
            data = ""
            decode_data = " "
            t = time.time()
            cont = False
            while True:
                print('start reading...')
                # self.delay(2)
                try:
                    data = self.terminal.readline()
                    decode_data = str(data.decode("utf-8"))
                    print(decode_data)
                    if "y:" in decode_data or cont:
                        print('Receive: ' + decode_data)
                        break
                    elif (time.time() - t >= 10):  # count 10s, if no response set time out
                        print('[INFO] Timeout...')
                        break
                    else:
                        self.send_data(self.msg)
                except Exception:
                    self.send_data(self.msg)
            values = list(decode_data[3:].split(' '))
            try:
                values = list(map(lambda x: None if not is_float(x) else float(x), values))
            except Exception:
                values = list(map(lambda x: str(x), values))

            return values[:6]
        else:
            return ['nan'] * 6

    def send_data(self, data):
        '''send signal to arduino'''
        if self.available:
            print("Sent: " + data)
            data = bytearray(data, 'utf-8')
            self.terminal.write(data)

    def delay(self, t):
        time.sleep(t)

    def stop(self):
        if self.available:
            self.send_data("x: end")
            self.terminal.close()
