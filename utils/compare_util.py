import numpy as np

def face_distance(face_encodings, face_to_compare):
    """
    计算两个人脸特征向量之间的欧式距离，并返回结果
    :param face_encodings: np.array, shape为(N, 512)，包含N个人脸特征向量
    :param face_to_compare: np.array, shape为(512,)，表示待比较的人脸特征向量
    :return: np.array, shape为(N,)，表示每个人脸特征向量与待比较特征向量的欧式距离
    """
    return np.linalg.norm(face_encodings - face_to_compare, axis=1)

def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    """
    将一个人脸特征向量与多个已知的人脸特征向量进行对比，返回所有对比结果中距离小于tolerance的结果
    :param known_face_encodings: np.array, shape为(N, 512)，包含N个已知的人脸特征向量
    :param face_encoding_to_check: np.array, shape为(512,)，表示待比较的人脸特征向量
    :param tolerance: float, 表示距离的允许误差，越小则越精确但可能会漏掉一些正确结果
    :return: np.array, shape为(M,)，表示与待比较特征向量距离小于tolerance的已知特征向量的下标
    """
    distances = face_distance(known_face_encodings, face_encoding_to_check)
    return np.where(distances <= tolerance)[0]
