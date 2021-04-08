import cv2
import numpy as np
import face_recognition
import os
import pickle
import time
import dlib

def face_check():
    className = []
    def findEndcodings():
        encodeList = []
        for pickleFile in os.listdir("Dataset/pickleFile"):
            with open(f"Dataset/pickleFile/{pickleFile}", "rb") as f:
                data = pickle.load(f)
                encodeList += data
                for i in range(len(data)):
                    className.append(pickleFile.split(".")[0])
        return encodeList

    endcodeListKnown = findEndcodings()
    # print(len(className))
    # print(len(endcodeListKnown))
    cap = cv2.VideoCapture(0)
    scale = 0.2
    unscale = int(1 / scale)
    start = time.time()
    while True:
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
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * unscale, x2 * unscale, y2 * unscale, x1 * unscale
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                    cap.release()
                    cv2.destroyAllWindows()
                    return True, name

        if time.time() - start > 15:
            print("Unknown !")
            cap.release()
            cv2.destroyAllWindows()
            return False, "Ko xác định !"
        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break


def encode_pickle():
    path = 'Dataset/boss'
    className = []

    for boss in os.listdir(path):
        if f"{boss}.pkl" in os.listdir("Dataset/pickleFile"):
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
        with open(f"Dataset/pickleFile/{boss}.pkl", "wb+") as f:
            pickle.dump(encodeList, f)

def face_register(name):
    detector = dlib.get_frontal_face_detector()

    amount_image_extract = 20
    amount_frame_pass = 10
    count_img = 0
    frame = 0
    cap = cv2.VideoCapture(0)
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    # size = (width, height)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('own_video.avi', fourcc, 24.0, size)
    count_save = 0
    try:
        os.mkdir(f"Dataset/boss/{name}")
    except:
        pass
    while True:
        frame += 1
        ret, img = cap.read()
        imgCopy = img.copy()
        # out.write(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        if len(faces) > 0:
            count_save += 1
            if count_save % 10 == 1:
                for face in faces:
                    x1, x2, y1, y2 = face.left(), face.right(), face.top(), face.bottom()
                    count_img += 1
                    cv2.rectangle(imgCopy, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        # imgCut = img[y1:y2, x1:x2]
                    cv2.imwrite(f"Dataset/boss/{name}/Face_{count_img}.jpg", img)
                    print(f"Saving img {count_img}")
        cv2.imshow("Video", imgCopy)
        if cv2.waitKey(1) & 0xff == ord("q"):
            break
        if count_img >= 20:
            cap.release()
            cv2.destroyAllWindows()
            break

