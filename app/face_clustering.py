import os
from typing import List

from imutils import build_montages
import cv2
import numpy as np
from sklearn.cluster import DBSCAN
import face_recognition

from app.face_detection import facelib_cnn_detection
from app.utils import clean_destination


def encode_faces(faces_path: str, limit_files=None) -> List[dict]:
    out = []
    files_processed = 0
    for root, dirs, files in os.walk(faces_path):
        for image_name in files:
            files_processed += 1
            if limit_files is not None and files_processed > limit_files:
                break
            image_path = os.path.join(faces_path, image_name)
            faces = facelib_cnn_detection(image_path)[1]
            if len(faces):
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image, faces)
                d = [{"image_path": image_name, "location": box, "encoding": enc}
                     for (box, enc) in zip(faces, encodings)]
                out.extend(d)
    return out


def clustering_faces(faces_path: str, dst_filepath: str, encodings: List[dict]) -> int:
    clean_destination(dst_filepath)
    data = np.array(encodings)
    encodings = [d["encoding"] for d in data]

    clt = DBSCAN(metric="euclidean", n_jobs=-1, eps=0.35)
    clt.fit(encodings)

    label_ids = np.unique(clt.labels_)
    unique_faces_found = len(np.where(label_ids > -1)[0])

    # save clusters montage to output path
    for cluster_id in label_ids:
        idxs = np.where(clt.labels_ == cluster_id)[0]
        idxs = np.random.choice(idxs, size=min(25, len(idxs)),
                                replace=False)
        faces = []
        for i in idxs:
            image_path = os.path.join(faces_path, data[i]["image_path"])
            image = cv2.imread(image_path)
            (top, right, bottom, left) = data[i]["location"]
            face = image[top:bottom, left:right]
            face = cv2.resize(face, (96, 96))
            faces.append(face)
        montage = build_montages(faces, (96, 96), (5, 5))[0]
        cv2.imwrite(os.path.join(dst_filepath, '%s.jpg' % cluster_id), montage)

    return unique_faces_found
