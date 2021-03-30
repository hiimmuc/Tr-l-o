# face detection for the 5 Celebrity Faces Dataset
import glob
import os
from os import listdir
from os.path import isdir

import cv2
import numpy as np
from faceNet import FaceNet
from matplotlib import pyplot as plt
from numpy import asarray, expand_dims, load, savez_compressed
from PIL import Image
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.preprocessing import LabelEncoder, Normalizer
from sklearn.svm import SVC
from sklearn.utils import shuffle
from tensorflow.keras.models import load_model
from tqdm import tqdm


def load_datasets(directory, size=(224, 224)):
    faces, Y = list(), list()
    labels = ['boss']
    for dir_ in os.listdir(directory):
        for img in os.listdir(os.path.join(directory, dir_)):
            path = os.path.join(os.path.join(directory, dir_), img)
            image = Image.open(path)
            image = image.convert('RGB')
            pixels = asarray(image)
            # resize to required size
            image = Image.fromarray(pixels)
            image = image.resize(size)
            face_array = asarray(image)

            faces.append(face_array)
            Y.append(directory)

    return asarray(faces), asarray(Y)


class Embedding():
    def __init__(self, model_path, weight_path):
        self.model_path = model_path
        self.weight_path = weight_path
        self.net = self.creat_net()

        pass

    def creat_net(self):
        model = load_model(self.model_path)
        model.summary()
        model.load_weights(self.weight_path)
        return model

    def embedding(self, face_pixels):
        # scale pixel values
        face_pixels = face_pixels.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        # transform face into one sample
        samples = expand_dims(face_pixels, axis=0)
        # make prediction to get embedding
        yhat = self.net.predict(samples)
        return yhat[0]

    def get_embedding(self, ds_set):
        embedding_vectors = []
        for face_pixels in ds_set:
            face_pixels = cv2.resize(face_pixels, (160, 160))
            embedding_vector = self.embedding(face_pixels)
            embedding_vectors.append(embedding_vector)
        return asarray(embedding_vectors)

    def embbedding_model(self, filepath, savedir):

        # load train dataset
        image, label = load_datasets(filepath, size=(160, 160))

        savepath = f'{savedir}/using_face_dataset.npz'
        savez_compressed(savepath, image, label)

        # load the face dataset
        data = load(savepath, mmap_mode='r+', allow_pickle=True)
        images, label = data['arr_0'], data['arr_1']

        # load the facenet model to an embedding
        emb_imgs = self.get_embedding(images)

        # save arrays to one file in compressed format
        savez_compressed(f'{savedir}/faces-embeddings.npz', emb_imgs, label)

    def calc_emb_test(self, faces):
        pd = []
        for face in faces:
            pd.append(self.embedding(face))
        # embs = l2_normalize(np.concatenate(pd))
        embs = np.array(pd)
        return np.array(embs)


# model_path = r'keras-facenet/model/facenet_keras.h5'
# weight_path = r"keras-facenet/weights/facenet_keras_weights.h5"
# filepath = r'dataset/boss'
# save_emb = r'dataset'
# emb = Embedding(model_path, weight_path)
# emb.embbedding_model(filepath, save_emb)
