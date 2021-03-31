import os
import time

import pyfirmata
import serial


class ArduinoConfig():
    def __init__(self, com):
        super(ArduinoConfig, self).__init__()
        self.board = pyfirmata.Arduino(com)

        self.iteration = pyfirmata.util.Iterator(self.board)
        self.iteration.start()
        # self.terminal = serial.Serial(com, baudrate=9600)
        self.terminal = ''
        self.port = {
            'input': {
                'thermal': [1, self.board.get_pin('a:1:i')],
                'proximity': [2, self.board.get_pin('a:2:i')],
                'Humidity': [3, self.board.get_pin('a:3:i')],
                'lights': [4, self.board.get_pin('a:4:i')],
                'digital': [5, self.board.get_pin('d:5:i')],
                'dust':
                [self.board.get_pin('a:0:i'),
                 self.board.get_pin('d:2:o')]
            },
            'output': {
                'fan': [5, self.board.get_pin('a:5:p')],
                'led': [6, self.board.get_pin('d:6:p')]
            }
        }

    def get_data_port(self, about):
        pipeline = self.port['input'][about][1]
        value = pipeline.read()
        return value if value is not None else 0

    def get_data_terminal(self):
        data = self.terminal.readline()
        decode_data = str(data.decode("utf-8"))
        values = decode_data.split(' ')
        values = list(lambda: float(x) for x in values)
        return values

    def transfer_data_port(self, type, data):
        pipeline = self.port['output'][type][1]
        pipeline.write(data)

    def transfer_data_terminal(self, data):
        self.terminal.write(data)

    def delay(self, t):
        time.sleep(t)

    def stop(self):
        self.terminal.close()
