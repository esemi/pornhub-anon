import logging

from app.face_detection import extract_faces, cascade_detection
from app.video_to_frame import extract_frames, av_converter

TEST_VIDEO_FILE = '/home/esemi/Downloads/prod.mp4'
TEST_FRAMES_FOLDER = '/home/esemi/pornhub-anon-tmp/frames'
TEST_FACES_FOLDER = '/home/esemi/pornhub-anon-tmp/faces'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    frames_count = extract_frames(TEST_VIDEO_FILE, TEST_FRAMES_FOLDER, av_converter)
    logging.info('extracted %d frames', frames_count)

    faces_count = extract_faces(TEST_FRAMES_FOLDER, TEST_FACES_FOLDER, cascade_detection)
    logging.info('filtered %d faces', faces_count)
