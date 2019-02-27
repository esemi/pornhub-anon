import unittest

from app.face_clustering import encode_faces, clustering_faces
from app.utils import clean_destination

TEST_FACES_FOLDER = './source/faces'
TEST_FRAMES_FOLDER = './tmp/%s'


class TestEncoding(unittest.TestCase):
    def test_smoke(self):
        res = encode_faces(TEST_FACES_FOLDER, limit_files=3)
        self.assertEqual(4, len(res))
        for i in res:
            self.assertIn('image_path', i)
            self.assertIn('location', i)
            self.assertIn('encoding', i)


class TestClustering(unittest.TestCase):
    def test_smoke(self):
        encodings = encode_faces(TEST_FACES_FOLDER, limit_files=20)
        clean_destination(TEST_FRAMES_FOLDER % 'clusters')
        res = clustering_faces(TEST_FACES_FOLDER, TEST_FRAMES_FOLDER % 'clusters', encodings)
        self.assertEqual(1, res)
