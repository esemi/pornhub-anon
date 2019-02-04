from typing import Tuple

import face_recognition


def facelib_hog_detection(filepath: str) -> Tuple[int, list]:
    image = face_recognition.load_image_file(filepath)
    face_locations = face_recognition.face_locations(image)
    return len(face_locations), face_locations


def facelib_cnn_detection(filepath: str) -> Tuple[int, list]:
    image = face_recognition.load_image_file(filepath)
    face_locations = face_recognition.face_locations(image, model='cnn')
    return len(face_locations), face_locations


def facelib_show_face(filepath: str, detection_func):
    from PIL import Image, ImageDraw

    image = face_recognition.load_image_file(filepath)
    face_locations = detection_func(filepath)[1]

    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    for i, (top, right, bottom, left) in enumerate(face_locations):
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
    del draw

    if face_locations:
        pil_image.show()
