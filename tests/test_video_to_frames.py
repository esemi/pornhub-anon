import shutil
import unittest
from time import time

from app.utils import clean_destination
from app.video_to_frame import opencv_converter, ffmpeg_converter, av_converter

TEST_VIDEO_FILE = './source/videoplayback.mp4'
TEST_FRAMES_FOLDER = './tmp/%s'
EXPECTED_FRAMES_FROM_SAMPLE = 60
EXPECTED_FRAMES_EQUAL_FACTOR = 0.05


class TestConverters(unittest.TestCase):
    def test_all(self):
        for function in (opencv_converter, ffmpeg_converter, av_converter):
            clean_destination(TEST_FRAMES_FOLDER % function.__name__)
            res = function(TEST_VIDEO_FILE, TEST_FRAMES_FOLDER % function.__name__)
            self.assertAlmostEqual(EXPECTED_FRAMES_FROM_SAMPLE, res,
                                   delta=EXPECTED_FRAMES_FROM_SAMPLE * EXPECTED_FRAMES_EQUAL_FACTOR,
                                   msg='%s incomplete' % function.__name__)


class TestSpeed(unittest.TestCase):
    def test_complex(self):
        """
        opencv_converter function bench: 101.52 sec total; 1.02 sec avg
        ffmpeg_converter function bench: 114.36 sec total; 1.14 sec avg
        av_converter function bench:      70.01 sec total; 0.70 sec avg
        """
        number_tests = 100
        for function in (opencv_converter, ffmpeg_converter, av_converter):
            try:
                shutil.rmtree(TEST_FRAMES_FOLDER % function.__name__)
            except:
                pass

            # todo delete dst path
            start_time = time()
            for i in range(number_tests):
                clean_destination(TEST_FRAMES_FOLDER % function.__name__)
                function(TEST_VIDEO_FILE, TEST_FRAMES_FOLDER % function.__name__)
            print("%s function bench: %.2f sec total; %.2f sec avg" % (function.__name__,
                                                                       time() - start_time,
                                                                       (time() - start_time) / number_tests))
