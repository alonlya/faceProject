import unittest
import cv2

from utils import face_util


class TestFaceUtil(unittest.TestCase):

    def test_face_detection(self):
        img_raw = cv2.imread('/home/zoneyet/图片/test2.jpg')
        result = face_util.face_detection(img_raw)
        self.assertEqual(len(result), 1)

    def test_face_embedding(self):
        img_raw = cv2.imread('/home/zoneyet/图片/test2.jpg')
        embeddings = face_util.face_embedding(img_raw)
        self.assertEqual(embeddings.shape, (1, 512))


if __name__ == '__main__':
    unittest.main()
