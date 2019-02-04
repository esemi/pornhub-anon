import os
import unittest
from time import time

from app.face_detection import facelib_hog_detection, facelib_cnn_detection, facelib_show_face

TEST_FACES_FOLDER = './source/faces'
TEST_NOFACES_FOLDER = './source/no_faces'
TEST_FAILFACES_FILE = './source/fail_face_detect.jpg'


class TestDetectors(unittest.TestCase):
    def test_positive(self):
        for function in (facelib_hog_detection, facelib_cnn_detection):
            for root, dirs, files in os.walk(TEST_FACES_FOLDER):
                for i in files:
                    res = function(os.path.join(TEST_FACES_FOLDER, i))[0]
                    self.assertEqual(1, res, msg='%s incomplete' % function.__name__)

    def test_negative(self):
        for function in (facelib_cnn_detection, facelib_hog_detection):
            for root, dirs, files in os.walk(TEST_NOFACES_FOLDER):
                for i in files:
                    res = function(os.path.join(TEST_NOFACES_FOLDER, i))[0]
                    self.assertEqual(0, res, msg='%s incomplete (%s)' % (function.__name__, i))

    def test_fail(self):
        for function in (facelib_cnn_detection, facelib_hog_detection):
            res = function(TEST_FAILFACES_FILE)[0]
            self.assertGreater(res, 0, msg='%s incomplete' % function.__name__)
            facelib_show_face(TEST_FAILFACES_FILE, function)


class TestSpeed(unittest.TestCase):
    def test_complex(self):
        number_tests = 100
        for function in (facelib_hog_detection, facelib_cnn_detection):
            start_time = time()
            for i in range(number_tests):
                function(os.path.join(TEST_NOFACES_FOLDER, '0.jpg'))
            print("%s function bench: %.2f sec total; %.2f sec avg" % (function.__name__,
                                                                       time() - start_time,
                                                                       (time() - start_time) / number_tests))
