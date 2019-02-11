import logging
import os

from app.face_detection import extract_faces, cascade_detection
from app.video_to_frame import extract_frames, av_converter

TEST_SOURCE_FOLDER = '/home/esemi/pornhub-anon-tmp/sources'
TEST_FRAMES_FOLDER = '/home/esemi/pornhub-anon-tmp/frames'
TEST_FACES_FOLDER = '/home/esemi/pornhub-anon-tmp/faces'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    for root, dirs, files in os.walk(TEST_SOURCE_FOLDER):
        for i in files:
            logging.info('process %s image', i)
            image_num = i.split('.')[0]
            frames_count = extract_frames(os.path.join(TEST_SOURCE_FOLDER, i),
                                          os.path.join(TEST_FRAMES_FOLDER, image_num), av_converter)
            logging.info('extracted %d frames', frames_count)

            faces_count = extract_faces(os.path.join(TEST_FRAMES_FOLDER, image_num),
                                        os.path.join(TEST_FACES_FOLDER, image_num), cascade_detection)
            logging.info('filtered %d faces', faces_count)

