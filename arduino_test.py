import time

import arduinoConfig as arduino

com_path = "COM6"

myArduino = arduino.ArduinoConfig(com_path)
t = time.time()

print(myArduino.get_data())
myArduino.stop()
