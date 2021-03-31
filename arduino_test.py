import time

import arduinoConfig as arduino

com_path = "COM6"
myArduino = arduino.ArduinoConfig(com_path)
t = time.time()
while True:
    # sw = myArduino.get_data('input', 'thermal')
    # thr = 18
    # sw = (sw * 5000.0 - 500.0) / 10.0
    # print(sw, type(sw))
    # if sw >= thr:
    #     myArduino.transfer_data('output', 'led', 0.01)
    # else:
    #     myArduino.transfer_data('output', 'led', 0)
    # myArduino.transfer_data('output', 'led', 0.5)
    # myArduino.delay(0.1)
    # if time.time() - t >= 5.0:
    #     myArduino.transfer_data('output', 'led', 0)
    #     break
    data = myArduino.get_data_terminal()
    print(data)
    myArduino.stop()
    break
