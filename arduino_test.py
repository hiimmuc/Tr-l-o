import time

import arduinoConfig as arduino

com_path = "COM6"

myArduino = arduino.ArduinoConfig(com_path)
t = time.time()

print(myArduino.get_data())
myArduino.stop()
# myArduino.send_data('x: end\n')
# myArduino.send_data('1\n')

# data = myArduino.terminal.readline()
# decode_data = str(data.decode("utf-8"))
# # while len(decode_data.strip()) != 0:
# #     print(decode_data)
# #     data = myArduino.terminal.readline()
# #     decode_data = str(data.decode("utf-8"))
