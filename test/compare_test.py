import numpy as np
import unittest

from utils.compare_util import face_distance, compare_faces


class TestFaceComparison(unittest.TestCase):

    def test_face_distance(self):
        face_encoding_to_check = np.random.rand(512)
        known_face_encodings = np.random.rand(5, 512)
        tolerance = 0.6
        matches = compare_faces(known_face_encodings, face_encoding_to_check, tolerance)
        print(matches)

    def test_compare_faces(self):
        known_face_encodings = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]])
        face_encoding_to_check = np.array([0.5, 0.6, 0.7])
        tolerance = 0.4
        expected_result = np.array([1])
        result = compare_faces(known_face_encodings, face_encoding_to_check, tolerance)
        self.assertTrue(np.allclose(result, expected_result))
