from datetime import datetime
from typing import Tuple, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB
from model.face import FaceDatabase


class FaceDatabaseManager:
    def __init__(self):
        self.engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")
        self.Session = sessionmaker(bind=self.engine)

    def add_face(self, name: str, group: str, feature: bytes, face_base64: str = None) -> int:
        """
        添加人脸到数据库中
        :param name: 人脸对应姓名
        :param group: 人脸所属分组
        :param feature: 人脸特征向量
        :param face_base64: 人脸图片的Base64编码
        :return: 添加成功后的人脸ID
        """
        with self.Session() as session:
            face = FaceDatabase(
                name=name,
                group=group,
                face_feature=feature,
                face_base64=face_base64,
                created_time=datetime.now()
            )
            session.add(face)
            session.commit()
            return face.id

    def update_face(self, face_id: int, name: str = None, group: str = None, feature: bytes = None,
                    face_base64: str = None) -> bool:
        """
        更新数据库中的人脸信息
        :param face_id: 人脸ID
        :param name: 人脸对应姓名，可选
        :param group: 人脸所属分组，可选
        :param feature: 人脸特征向量，可选
        :param face_base64: 人脸图片的Base64编码，可选
        :return: 是否更新成功
        """
        with self.Session() as session:
            face = session.query(FaceDatabase).filter_by(id=face_id, is_deleted=False).first()
            if not face:
                return False
            if name is not None:
                face.name = name
            if group is not None:
                face.group = group
            if feature is not None:
                face.face_feature = feature
            if face_base64 is not None:
                face.face_base64 = face_base64
            face.updated_time = datetime.now()
            session.commit()
            return True

    def delete_face(self, face_id: int) -> bool:
        """
        删除数据库中的人脸信息
        :param face_id: 人脸 ID
        :return: 是否删除成功
        """
        with self.Session() as session:
            face = session.query(FaceDatabase).filter_by(id=face_id, is_deleted=False).first()
            if not face:
                return False
            face.is_deleted = True
            session.commit()
            return True

    def get_face_by_id(self, face_id: int) -> Tuple[str, str, bytes]:
        """
        根据 ID 获取人脸信息
        :param face_id: 人脸 ID
        :return: (姓名, 分组, 特征向量) 元组，若未找到则返回 None
        """
        with self.Session() as session:
            face = session.query(FaceDatabase).filter_by(id=face_id, is_deleted=False).first()
            if not face:
                return None
            return face.name, face.group, face.face_feature

    def get_face_list(self, page: int = 1, limit: int = 10, name: str = None, group: str = None) -> Tuple[List[Tuple[int, str, str, bytes]], int]:
        """
        分页查询人脸库中的人脸信息
        :param page: 分页页码，默认值为1
        :param limit: 每页限制条数，默认值为10
        :param name: 人脸名称，支持模糊查询
        :param group: 人脸分组，支持模糊查询
        :return: 包含人脸信息的列表，以及总共的记录数
        """
        with self.Session() as session:
            query = session.query(FaceDatabase).filter_by(is_deleted=False)
            if name:
                query = query.filter(FaceDatabase.name.like(f"%{name}%"))
            if group:
                query = query.filter(FaceDatabase.group.like(f"%{group}%"))
            total = query.count()
            faces = query.offset(page * limit).limit(limit).all()
            return [(f.id, f.name, f.group, f.face_feature) for f in faces], total