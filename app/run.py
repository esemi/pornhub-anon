import logging
import os

from app.face_clustering import encode_faces, clustering_faces
from app.face_detection import extract_faces, cascade_detection
from app.video_to_frame import extract_frames, av_converter

TEST_SOURCE_FOLDER = '/tmp/xvideos-sources/'
TEST_FRAMES_FOLDER = '/home/esemi/pornhub-anon-tmp/frames'
TEST_FACES_FOLDER = '/home/esemi/pornhub-anon-tmp/faces'
TEST_CLUSTERS_FOLDER = '/home/esemi/pornhub-anon-tmp/clusters'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    for root, dirs, files in os.walk(TEST_SOURCE_FOLDER):
        for i in files:
            logging.info('process %s video file', i)
            image_uid = i.split('.')[0]
            frames_count = extract_frames(os.path.join(TEST_SOURCE_FOLDER, i),
                                          os.path.join(TEST_FRAMES_FOLDER, image_uid), av_converter)
            logging.info('extracted %d frames', frames_count)

            faces_count = extract_faces(os.path.join(TEST_FRAMES_FOLDER, image_uid),
                                        os.path.join(TEST_FACES_FOLDER, image_uid), cascade_detection)
            logging.info('filtered %d frames w/ faces', faces_count)

            encoded_faces = encode_faces(os.path.join(TEST_FACES_FOLDER, image_uid))
            logging.info('encoded %d faces', len(encoded_faces))

            unique_faces = clustering_faces(os.path.join(TEST_FACES_FOLDER, image_uid),
                                            os.path.join(TEST_CLUSTERS_FOLDER, image_uid), encoded_faces)
            logging.info('clustered %d unique faces', unique_faces)

