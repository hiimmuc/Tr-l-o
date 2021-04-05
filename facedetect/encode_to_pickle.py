import cv2
import numpy as np
import face_recognition
import os
import time
import pickle

path = 'dataset/boss'
className = []
directory = os.listdir(path)

for boss in os.listdir(path):
    if f"{boss}.pkl" in os.listdir("dataset/pickleFile"):
        continue
    print(f"Encoding {boss}")
    images = []
    myList = os.listdir(f'{path}/{boss}')
    count = 0
    for cl in myList:
        curImg = cv2.imread(f'{path}/{boss}/{cl}')
        images.append(curImg)
        count += 1
        if count >= 20:
                break
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except:
            pass
    with open(f"dataset/pickleFile/{boss}.pkl", "wb+") as f:
        pickle.dump(encodeList, f)