# import the necessary packages
import glob
import os
import time

import cv2
import imutils
import numpy as np
from imutils.video import FPS, VideoStream
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from videoAccelerate import *


class FaceNet(object):
    def __init__(self, prototxt_path, weights_path):
        super(FaceNet, self).__init__()
        self.prototxt_path = prototxt_path
        self.weights_path = weights_path

    def creat_net(self):
        t = time.time()
        print("[INFO] read face net")
        self.face_net = cv2.dnn.readNet(self.prototxt_path, self.weights_path)
        print("[INFO] done loading!")
        print(time.time() - t)
        # return self.face_net, self.mask_net

    def detector(self, frame, confidence_base=0.8, crop_scale=0.05):
        # initialize our list of faces, their corresponding locations,
        # and the list of predictions from our face mask network
        faces = []
        locs = []
        # grab the dimensions of the frame and then construct a blob
        # from it
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), swapRB=True)

        # pass the blob through the network and obtain the face detections
        self.face_net.setInput(blob)
        detections = self.face_net.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the detection
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the confidence is
            # greater than the minimum confidence
            if confidence > confidence_base:
                # compute the (x, y)-coordinates of the bounding box for
                # the object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # ensure the bounding boxes fall within the dimensions of
                # the frame
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
                locs.append([startX, startY, endX, endY])

                w, h = abs(endX - startX), abs(endY - startY)
                startX = int(startX - crop_scale * w)
                startY = int(startY - crop_scale * h)
                endX = int(endX + crop_scale * w)
                endY = int(endY + crop_scale * h)
                faces.append(np.asarray(frame[startY:endY, startX:endX]))

                # display the label and bounding box rectangle on the output
                # frame
                color = (0, 255, 0)
                cv2.putText(frame,
                            "face", (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            color,
                            1,
                            lineType=cv2.LINE_AA)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        return frame, faces, locs

    def get_video(self,
                  user_name,
                  source=0,
                  save_loc=r'./save_vid',
                  detect=False):
        # initialize the video stream
        file_name = os.path.join(save_loc, f'{user_name}.avi')
        if os.path.exists(file_name):
            os.remove(file_name)
        print("[INFO] starting video stream...")

        # stream = cv2.VideoCapture(source)
        vid_get = VideoGet(source).start()
        fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        writer = cv2.VideoWriter(file_name, fourcc, 150.0, (640, 480))
        fps = FPS().start()
        # loop over the frames from the video stream
        while True:
            frame = vid_get.frame
            grab = vid_get.grabbed
            if grab:
                if detect:
                    frame, _, _ = self.detector(frame, crop_scale=0.05)

                # show the output frame
                cv2.imshow("Frame", frame)
                writer.write(frame)
                fps.update()

                # if the `q` key was pressed, break from the loop
            if cv2.waitKey(1) == 27:
                break

        fps.stop()
        vid_get.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        writer.release()
        cv2.destroyAllWindows()

    def extractFromVid(self, source=0, save_path=""):
        # initialize the video stream

        print("[INFO] starting video stream...")
        if source != 0:
            videos = glob.glob(os.path.join(source, '*.avi'))
        videos = source if source == 0 else videos
        save_imgs = []
        exist_name = os.listdir(save_path)
        for vid in videos:
            if any(name in vid for name in exist_name):
                print('da co ten')
                continue
            stream = cv2.VideoCapture(vid)

            fps = FPS().start()
            # loop over the frames from the video stream
            while True:
                ret, frame = stream.read()
                if ret:
                    frame, faces, _ = self.detector(frame,
                                                    confidence_base=0.5,
                                                    crop_scale=0.05)
                    for face in faces:
                        save_imgs.append(face)
                    # show the output frame
                    cv2.imshow("Frame", frame)
                    fps.update()

                    # if the `q` key was pressed, break from the loop
                if cv2.waitKey(1) == 27 or not ret:
                    break

            fps.stop()
            print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

            stream.release()
            cv2.destroyAllWindows()
            print(len(save_imgs), type(save_imgs))
            # do a bit of cleanup
            if len(save_path) != 0:
                step = int(fps.fps() * 2)
                step = step if (step > 0) else 5
                count = 0
                for i in range(0, len(save_imgs), step):
                    cv2.imwrite(os.path.join(save_path, f"home{count}.jpg"),
                                save_imgs[i])
                    count += 1
                print(f"DONE saving faces: {len(os.listdir(save_path))}")
            pass


# # load our serialized face detector model from disk
# prototxtPath = r"backup\deploy.prototxt"
# weightsPath = r"backup\res10_300x300_ssd_iter_140000.caffemodel"

# model = FaceNet(prototxt_path=prototxtPath, weights_path=weightsPath)
# model.creat_net()
# model.extractFromVid(source=r"./save_vid", save_path=r"dataset/boss")
