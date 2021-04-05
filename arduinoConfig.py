import time

import serial


class ArduinoConfig():
    def __init__(self, com):
        super(ArduinoConfig, self).__init__()
        self.com = com
        self.available = True
        try:
            self.terminal = serial.Serial(self.com, baudrate=9600)
        except Exception:
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
            self.send_data("x: get")
            data = ""
            decode_data = " "
            t = time.time()
            cont = False
            while True:
                data = self.terminal.readline()
                decode_data = str(data.decode("utf-8"))
                print(decode_data)
                if "y:" in decode_data or cont:
                    print('Receive: ' + decode_data)
                    break
                elif (time.time() - t >= 15):  # count 10s, if no response set time out
                    print('[INFO] Timeout...')
                    break
                else:
                    self.delay(3)
                    self.send_data("x: get")
            values = list(decode_data[3:].split(' '))
            try:
                values = list(map(lambda x: None if not is_float(x) else float(x), values))
            except Exception:
                values = list(map(lambda x: str(x), values))

            return values[:6]
        else:
            return 'Error'

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
