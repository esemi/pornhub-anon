import shutil
import unittest
from time import time

from app.video_to_frame import opencv_converter, ffmpeg_converter, av_converter

TEST_VIDEO_FILE = './source/videoplayback.mp4'
TEST_FRAMES_FOLDER = './tmp/%s'
EXPECTED_FRAMES_FROM_SAMPLE = 60
EXPECTED_FRAMES_EQUAL_FACTOR = 0.05


class TestConverters(unittest.TestCase):
    def test_all(self):
        for function in (opencv_converter, ffmpeg_converter, av_converter):
            res = function(TEST_VIDEO_FILE, TEST_FRAMES_FOLDER % function.__name__)
            self.assertAlmostEqual(EXPECTED_FRAMES_FROM_SAMPLE, res,
                                   delta=EXPECTED_FRAMES_FROM_SAMPLE * EXPECTED_FRAMES_EQUAL_FACTOR,
                                   msg='%s incomplete' % function.__name__)


class TestSpeed(unittest.TestCase):
    def test_complex(self):
        number_tests = 100
        for function in (opencv_converter, ffmpeg_converter, av_converter):
            try:
                shutil.rmtree(TEST_FRAMES_FOLDER % function.__name__)
            except:
                pass

            # todo delete dst path
            start_time = time()
            for i in range(number_tests):
                function(TEST_VIDEO_FILE, TEST_FRAMES_FOLDER % function.__name__)
            print("%s function bench: %.2f sec total; %.2f sec avg" % (function.__name__,
                                                                       time() - start_time,
                                                                       (time() - start_time) / number_tests))
