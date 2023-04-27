
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FaceDatabase(Base):
    __tablename__ = 'face_database'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    group = Column(String(128), nullable=False)
    face_feature = Column(LargeBinary, nullable=False)
    created_time = Column(DateTime, nullable=False)
    updated_time = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    face_base64 = Column(Text, nullable=True, comment='人脸图片的Base64编码')

    metadata = Base.metadata
