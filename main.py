import os
import sys

import assistant
import cv2
import numpy as np
from assistant import MyAssistant
from imutils.video import FPS
from PIL import Image
from pygui import Ui_GUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, list)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        print("[INFO] Start recording...")
        try:
            cap = cv2.VideoCapture(0)
            # stream = VideoStream().start()
            self.fps = FPS().start()
            while self._run_flag:
                ret, frame = cap.read()
                if ret:
                    output_img = frame
                    self.change_pixmap_signal.emit(output_img, self.value)
                    self.fps.update()
            self.fps.stop()
            print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
            cv2.destroyAllWindows()
        except Exception:
            pass

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(Ui_GUI, VideoThread):
    def __init__(self, MainWindow) -> None:
        super().__init__()
        self.setupUi(MainWindow)
        self.friday = MyAssistant()
        self.pushButton.clicked.connect(self.start_app)
        self.pushButton_2.clicked.connect(self.stop_app)

    @pyqtSlot(np.ndarray, list)
    def update_all(self, cvimg, value=[0, 0, 0]):
        """Updates the image_label with a new opencv image"""
        pass

    def convert_cv_qt(self, cvimg):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    @pyqtSlot()
    def stop_app(self):
        self.friday.stop()
        pass

    @pyqtSlot()
    def start_app(self):
        self.friday.run()
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App(MainWindow=MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
