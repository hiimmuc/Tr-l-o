import cv2
import dlib
import os


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
        os.mkdir(f"Dataset/Boss/{name}")
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
                    cv2.imwrite(f"Dataset/Boss/{name}/Face_{count_img}.jpg", img)
                    print(f"Saving img {count_img}")
        cv2.imshow("Video", imgCopy)
        if cv2.waitKey(1) & 0xff == ord("q"):
            break
        if count_img >= 20:
            break
    # if count_img >= amount_image_extract:
    #     cap.release()
    #     break

face_register("quang")