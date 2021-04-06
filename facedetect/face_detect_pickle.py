import os
import pickle
import time
from threading import Thread

import cv2
import face_recognition
import numpy as np

path = 'dataset/boss'
className = []
directory = os.listdir(path)


def findEndcodings():
    encodeList = []
    for pickleFile in os.listdir(r"dataset/pickleFile"):
        with open(f"dataset/pickleFile/{pickleFile}", "rb") as f:
            data = pickle.load(f)
            encodeList += data
            for i in range(len(data)):
                className.append(pickleFile.split(".")[0])
    return encodeList


# print(len(className))
# print(len(endcodeListKnown))


def face_check():
    cap = cv2.VideoCapture(0)
    scale = 0.2
    unscale = int(1 / scale)
    endcodeListKnown = findEndcodings()

    while True:
        start = time.time()
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, scale, scale)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(endcodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(endcodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = className[matchIndex].upper()
                if faceDis[matchIndex] < 0.4:
                    print(f"Welcome {name}")
                    print("Accuracy: ", faceDis[matchIndex])
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * unscale, x2 * unscale, y2 * unscale, x1 * unscale
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                    return 1

                else:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * unscale, x2 * unscale, y2 * unscale, x1 * unscale
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "UNKNOWN", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

        cv2.imshow('Video', img)
        print("Time:", time.time() - start)

        if cv2.waitKey(1) & 0XFF == ord('q'):
            break


face_check()
