import os
import time
from threading import Thread

import cv2
import face_recognition
import imutils
import numpy as np
from faceNet import FaceNet
from imutils.video import FPS, VideoStream
from videoAccelerate import *

path = r"dataset/boss"
images = []
className = ['boss']
directory = os.listdir(path)
threshold_distance = 0.8

print("Loading face encode ...")
for i in range(len(directory)):
    curImg = cv2.imread(f'{path}/{directory[i]}')
    images.append(curImg)


def findEndcodings(images):
    count = 0
    encodeList = []
    for img in images:
        count += 1
        print(f"Loading image {count}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except Exception:
            pass
    return encodeList


endcodeListKnown = findEndcodings(images)
count = 0
scale = 0.2
unscale = int(1 / scale)


def video_test(model, source):
    # initialize the video stream

    print("[INFO] starting video stream...")

    # stream = cv2.VideoCapture(source)
    vid_get = VideoGet(source).start()
    fps = FPS().start()
    end = False
    # loop over the frames from the video stream
    while True:
        frame = vid_get.frame
        grab = vid_get.grabbed
        if grab:
            frame_with_box, faces, locs = model.detector(frame, crop_scale=0.05)
            encode_frame = face_recognition.face_encodings(frame, locs)
            for encode_face, face_loc in zip(encode_frame, locs):
                matches = face_recognition.compare_faces(endcodeListKnown, encode_face)
                faceDis = face_recognition.face_distance(endcodeListKnown, encode_face)
                matchIndex = np.argmin(faceDis)
                print(matchIndex, faceDis)
                if matches[matchIndex]:
                    if faceDis[matchIndex] < threshold_distance:
                        print(1)
                        print("Welcome boss")
                        print("Closing program !")
                        end = True
                    else:
                        print(0)

            # show the output frame
            cv2.imshow("Frame", frame_with_box)
            fps.update()

            # if the `q` key was pressed, break from the loop
        if cv2.waitKey(1) == 27 or end or not grab:
            break

    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    cv2.destroyAllWindows()


# load our serialized face detector model from disk
prototxtPath = r"backup\deploy.prototxt"
weightsPath = r"backup\res10_300x300_ssd_iter_140000.caffemodel"


model = FaceNet(prototxt_path=prototxtPath, weights_path=weightsPath)
model.creat_net()
video_test(model, 0)
