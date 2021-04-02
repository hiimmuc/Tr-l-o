import os
import time
from threading import Thread

import cv2
import face_recognition
import numpy as np

path = r'.\dataset\boss'
images = []
className = []
directory = os.listdir(path)
threshold_distance = 0.45

print("Loading face encode ...")
for i in range(len(directory)):
    myList = os.listdir(os.path.join(path, directory[i]))
    for cl in myList:
        curImg = cv2.imread(f'{path}/{directory[i]}/{cl}')
        images.append(curImg)
        className.append(directory[i])


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


def main():
    endcodeListKnown = findEndcodings(images)

    count = 0
    scale = 0.2
    unscale = int(1 / scale)
    cap = cv2.VideoCapture(0)

    true_boss = 0
    while True:
        ret, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, scale, scale)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(endcodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(endcodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                if faceDis[matchIndex] < threshold_distance:
                    true_boss = 1
                    print(1)
                    print("Welcome boss")
                    print("Closing program !")
                    time.sleep(5)
                    break
                else:
                    print(0)
        if true_boss == 1:
            break
        cv2.imshow("Video", img)
        key = cv2.waitKey(1)
        if key == 27:
            break


main()
