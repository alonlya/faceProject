import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB
from model.face import FaceDatabase
from utils.db import FaceDatabaseManager


class TestFaceDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")
        self.Session = sessionmaker(bind=self.engine)
        self.manager = FaceDatabaseManager()

    def tearDown(self):
        with self.Session() as session:
            session.query(FaceDatabase).delete()
            session.commit()

    def test_add_face(self):
        name = "test_name"
        group = "test_group"
        feature = b"\x00\x01\x02\x03"
        face_base64 = "test_base64"
        face_id = self.manager.add_face(name, group, feature, face_base64)
        with self.Session() as session:
            face = session.query(FaceDatabase).filter_by(id=face_id).first()
            self.assertIsNotNone(face)
            self.assertEqual(face.name, name)
            self.assertEqual(face.group, group)
            self.assertEqual(face.face_feature, feature)
            self.assertIsNotNone(face.created_time)
            self.assertIsNone(face.updated_time)
            self.assertFalse(face.is_deleted)

    def test_update_face(self):
        name1 = "test_name1"
        group1 = "test_group1"
        feature1 = b"\x00\x01\x02\x03"
        face_base641 = "test_base641"
        face_id = self.manager.add_face(name1, group1, feature1, face_base641)
        name2 = "test_name2"
        group2 = "test_group2"
        feature2 = b"\x03\x02\x01\x00"
        face_base64 = "test_base642"
        self.assertTrue(self.manager.update_face(face_id, name2, group2, feature2, face_base64))
        with self.Session() as session:
            face = session.query(FaceDatabase).filter_by(id=face_id).first()
            self.assertIsNotNone(face)
            self.assertEqual(face.name, name2)
            self.assertEqual(face.group, group2)
            self.assertEqual(face.face_feature, feature2)
            self.assertIsNotNone(face.created_time)
            self.assertIsNotNone(face.updated_time)
            self.assertTrue(face.updated_time > face.created_time)
            self.assertFalse(face.is_deleted)

    def test_delete_face(self):
        name = "test_name"
        group = "test_group"
        feature = b"\x00\x01\x02\x03"
        face_id = self.manager.add_face(name, group, feature)
        self.assertTrue(self.manager.delete_face(face_id))
        with self.Session() as session:
            face = session.query(FaceDatabase).filter_by(id=face_id).first()
            self.assertIsNotNone(face)
            self.assertTrue(face.is_deleted)

    def test_get_face_by_id(self):
        name = "test_name"
        group = "test_group"
        feature = b"\x00\x01\x02\x03"
        face_id = self.manager.add_face(name, group, feature)
        self.assertEqual(self.manager.get_face_by_id(face_id), (name, group, feature))

    def test_get_face_by_nonexistent_id(self):
        self.assertIsNone(self.manager.get_face_by_id(-1))

    def test_get_face_list_no_filter(self):
        # 测试没有任何筛选条件的情况
        # 添加一些人脸数据
        for i in range(15):
            name = f"test_name{i}"
            group = f"test_group{i % 3}"
            feature = bytes([i % 256 for _ in range(128)])
            self.manager.add_face(name, group, feature)
        # 获取第一页的数据
        faces, total = self.manager.get_face_list()
        self.assertEqual(total, 15)
        self.assertEqual(len(faces), 10)
        self.assertEqual(faces[0][0], "test_name0")
        self.assertEqual(faces[-1][0], "test_name9")

        # 获取第二页的数据
        faces, total = self.manager.get_face_list(page=2)
        self.assertEqual(total, 15)
        self.assertEqual(len(faces), 5)
        self.assertEqual(faces[0][0], "test_name10")
        self.assertEqual(faces[-1][0], "test_name14")

    def test_get_face_list_with_name(self):
        # 测试按名称筛选的情况
        # 添加一些人脸数据
        for i in range(15):
            name = f"test_name{i}"
            group = f"test_group{i % 3}"
            feature = bytes([i % 256 for _ in range(128)])
            self.manager.add_face(name, group, feature)
        # 获取包含 "name1" 的数据
        faces, total = self.manager.get_face_list(name="name1")
        self.assertEqual(total, 1)
        self.assertEqual(len(faces), 1)
        self.assertEqual(faces[0][0], "test_name1")

    def test_get_face_list_with_group(self):
        # 测试按分组筛选的情况
        # 添加一些人脸数据
        for i in range(15):
            name = f"test_name{i}"
            group = f"test_group{i % 3}"
            feature = bytes([i % 256 for _ in range(128)])
            self.manager.add_face(name, group, feature)
        # 获取分组为 "test_group1" 的数据
        faces, total = self.manager.get_face_list(group="test_group1")
        self.assertEqual(total, 5)
        self.assertEqual(len(faces), 5)
        self.assertEqual(faces[0][0], "test_name1")
        self.assertEqual(faces[-1][0], "test_name13")

    def test_get_face_list_with_name_and_group(self):
        # 测试按名称和分组筛选的情况
        # 添加一些人脸数据
        for i in range(15):
            name = f"test_name{i}"
            group = f"test_group{i % 3}"
            feature = bytes([i % 256 for _ in range(128)])
            self.manager.add_face(name, group, feature)
        # 获取名称包含 "name1" 且分组为 "test_group1" 的数据
        faces, total = self.manager.get_face_list(name="name1", group="test_group1")
        self.assertEqual(total, 3)

if __name__ == '__main__':
    unittest.main()