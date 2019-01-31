import shutil
import unittest
from time import time

from app.video_to_frame import opencv_converter

TEST_VIDEO_FILE = './source/videoplayback.mp4'
TEST_FRAMES_FOLDER = '/tmp/pornhub-anon-tests/video_to_frames_unittests'


class TestOpenCV(unittest.TestCase):
    def test_smoke(self):
        res = opencv_converter(TEST_VIDEO_FILE, TEST_FRAMES_FOLDER)
        self.assertEqual(68, res)


class TestSpeed(unittest.TestCase):
    def test_complex(self):
        number_tests = 50
        for function in (opencv_converter, ):
            try:
                shutil.rmtree(TEST_FRAMES_FOLDER)
            except:
                pass

            # todo delete dst path
            start_time = time()
            for i in range(number_tests):
                function(TEST_VIDEO_FILE, TEST_FRAMES_FOLDER)
            print("%s function bench: %.2f sec total; %.2f sec avg" % (function.__name__,
                                                                       time() - start_time,
                                                                       (time() - start_time) / number_tests))
