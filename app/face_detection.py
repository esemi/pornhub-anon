import os
import shutil
from typing import Tuple

import face_recognition

from config import HAAR_CASCADE_XML, LBP_CASCADE_XML
from utils import clean_destination


def facelib_hog_detection(filepath: str) -> Tuple[int, list]:
    image = face_recognition.load_image_file(filepath)
    face_locations = face_recognition.face_locations(image, 2)
    return len(face_locations), face_locations


def facelib_cnn_detection(filepath: str) -> Tuple[int, list]:
    image = face_recognition.load_image_file(filepath)
    face_locations = face_recognition.face_locations(image, model='cnn')
    return len(face_locations), face_locations


def opencv_haar_detection(filepath: str) -> Tuple[int, list]:
    import cv2

    haar_face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_XML)
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = haar_face_cascade.detectMultiScale(gray)
    return len(faces), faces


def opencv_lbp_detection(filepath: str) -> Tuple[int, list]:
    import cv2

    lbp_face_cascade = cv2.CascadeClassifier(LBP_CASCADE_XML)
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = lbp_face_cascade.detectMultiScale(gray)
    return len(faces), faces


def cascade_detection(filepath: str) -> Tuple[int, list]:
    if all([opencv_lbp_detection(filepath)[0], opencv_haar_detection(filepath)[0], facelib_hog_detection(filepath)[0]]):
        return facelib_cnn_detection(filepath)
    return 0, []


def extract_faces(frames_path: str, faces_path: str, detection_function) -> int:
    clean_destination(faces_path)
    faces_counter = 0
    for root, dirs, files in os.walk(frames_path):
        for i in files:
            if detection_function(os.path.join(frames_path, i))[0]:
                shutil.copy(os.path.join(frames_path, i), faces_path)
                faces_counter += 1
    return faces_counter
