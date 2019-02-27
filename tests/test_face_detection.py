import os
import unittest
from time import time

from app.face_detection import (facelib_hog_detection, facelib_cnn_detection, show_face_image, opencv_haar_detection,
                                opencv_lbp_detection, cascade_detection)

TEST_FACES_FOLDER = './source/faces'
TEST_NOFACES_FOLDER = './source/no_faces'
DEBUG_MODE = False

ALL = (opencv_haar_detection, opencv_lbp_detection, facelib_hog_detection, facelib_cnn_detection, cascade_detection)


class TestDetectors(unittest.TestCase):
    def test_positive(self):
        """
        opencv_haar_detection function positive test: 100 total; 85 success; success rate: 0.85
        opencv_lbp_detection function positive test: 100 total; 79 success; success rate: 0.79
        facelib_hog_detection function positive test: 100 total; 84 success; success rate: 0.84
        facelib_cnn_detection function positive test: 100 total; 77 success; success rate: 0.77
        cascade_detection function positive test: 100 total; 77 success; success rate: 0.77
        """
        for function in ALL:
            success_detected = 0
            total_images = 0
            for root, dirs, files in os.walk(TEST_FACES_FOLDER):
                for i in files:
                    total_images += 1
                    res = function(os.path.join(TEST_FACES_FOLDER, i))[0]
                    if res == 1:
                        success_detected += 1
            self.assertEqual(100, total_images)
            self.assertAlmostEqual(0.8, float(success_detected) / float(total_images), delta=0.15)
            print("%s function positive test: %d total; %d success; success rate: %.2f" %
                  (function.__name__, total_images, success_detected,
                   float(success_detected) / float(total_images)))

    def test_negative(self):
        """
        opencv_haar_detection function negative test: 12 total; 8 success; success rate: 0.67
        opencv_lbp_detection function negative test: 12 total; 11 success; success rate: 0.92
        facelib_hog_detection function negative test: 12 total; 11 success; success rate: 0.92
        facelib_cnn_detection function negative test: 12 total; 11 success; success rate: 0.92
        cascade_detection function negative test: 12 total; 11 success; success rate: 0.92
        """
        for function in ALL:
            success_detected = 0
            total_images = 0
            for root, dirs, files in os.walk(TEST_NOFACES_FOLDER):
                for i in files:
                    total_images += 1
                    res = function(os.path.join(TEST_NOFACES_FOLDER, i))[0]
                    if not res:
                        success_detected += 1
            print("%s function negative test: %d total; %d success; success rate: %.2f" %
                  (function.__name__, total_images, success_detected,
                   float(success_detected) / float(total_images)))


class TestSpeed(unittest.TestCase):
    def test_complex(self):
        """
        opencv_haar_detection function bench: 3.04 sec total; 0.03 sec avg
        opencv_lbp_detection function bench: 0.49 sec total; 0.00 sec avg
        facelib_hog_detection function bench: 13.31 sec total; 0.13 sec avg
        facelib_cnn_detection function bench: 97.34 sec total; 0.97 sec avg
        cascade_detection function bench: 115.80 sec total; 1.16 sec avg
        """
        number_tests = 100
        for function in ALL:
            start_time = time()
            for i in range(number_tests):
                function(os.path.join(TEST_FACES_FOLDER, 'George_W_Bush_0001.jpg'))
            print("%s function bench: %.2f sec total; %.2f sec avg" % (function.__name__,
                                                                       time() - start_time,
                                                                       (time() - start_time) / number_tests))
