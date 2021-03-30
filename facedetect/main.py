import glob

import cv2
import numpy as np
from embbedding import Embedding
from faceNet import FaceNet
from imutils.video import FPS
from scipy.spatial import distance
from videoAccelerate import *

train_path = glob.glob(r"facedetect/dataset/boss")
nb_classes = len(train_path)


class Solution():
    def __init__(self, savepath):
        model_path = r'keras-facenet/model/facenet_keras.h5'
        weight_path = r"keras-facenet/weights/facenet_keras_weights.h5"
        filepath = r'dataset/boss'

        prototxtPath = r"backup\deploy.prototxt"
        weightsPath = r"backup\res10_300x300_ssd_iter_140000.caffemodel"

        self.model = FaceNet(prototxt_path=prototxtPath,
                             weights_path=weightsPath)
        self.model.creat_net()
        self.emb = Embedding(model_path, weight_path)
        self.data = load(savepath, mmap_mode='r+', allow_pickle=True)
        self.known_faces, self.label = self.data['arr_0'], self.data['arr_1']
        pass

    def run(self, source=0):
        print("[INFO] starting video stream...")

        # stream = cv2.VideoCapture(source)
        vid_get = VideoGet(source).start()
        fps = FPS().start()

        while True:
            frame = vid_get.frame
            grab = vid_get.grabbed
            distances = []
            if grab:
                frame_with_box, faces, locs = self.model.detector(
                    frame, crop_scale=0.05)
                for face in faces:
                    face = cv2.resize(face, (160, 160))
                encode_frame = self.emb.calc_emb_test(faces)

                for each_face in encode_frame:
                    each_face = each_face.reshape(-1)
                    for each_known in self.known_faces:
                        distances.append(
                            np.min(distance.euclidean(each_face, each_known)))
                label = ""
                if len(faces) != 0:
                    if np.min(distances) > 2.0:
                        label = "unknown"
                    else:
                        label = "Boss"
                    # show the output frame
                    frame_with_box = cv2.putText(frame_with_box, label,
                                                 (0, 20),
                                                 cv2.FONT_HERSHEY_SIMPLEX, 2,
                                                 (255, 0, 0))
                cv2.imshow("Frame", frame_with_box)
                fps.update()

                # if the `q` key was pressed, break from the loop
            if cv2.waitKey(1) == 27 or not grab:
                break
        print(np.min(distances))
        fps.stop()
        vid_get.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        cv2.destroyAllWindows()
        pass


sol = Solution(r'dataset/faces-embeddings.npz')
sol.run()
