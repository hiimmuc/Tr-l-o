from arduinoConfig import ArduinoConfig
from helpers import tools


class ProcessData():
    def __init__(self):
        super(ProcessData, self).__init__()
        self.myArduino = ArduinoConfig('COM6')
        self.myTools = tools()

    def process_data(self, txt_type, tag, targets=None):
        if txt_type == 'greeting':
            return self.greeting(tag, targets)
        elif txt_type == 'command':
            return self.do_command(tag, targets)
        elif txt_type == 'question':
            return self.ans_question(tag, targets)
        return None
        pass

    def ans_question(self, tag, targets=None):

        pass

    def do_command(self, tag, targets=None):
        if tag.lower() == 'bật':
            if targets in ['led', 'fan']:
                self.myArduino.send_data(f"x: {targets} on")
            if targets in ["word", 'excel', "gõ văn bản", "trình duyệt", "trình tìm kiếm", "youtube"]:
                self.myTools.open_application(targets)
            if targets in ['nhạc', 'music', "âm nhạc"]:
                self.myTools.play_music()
        if tag.lower() == 'tắt':
            self.myArduino.send_data(f"x: {targets} off")
        pass

    def greeting(self, tag, targets=None):
        pass
