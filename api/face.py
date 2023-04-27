import base64

import flask_cors
import numpy as np
from flask import Flask, jsonify, request
from utils.cache import RedisManager, FACE_KEY_INDEX
from utils.compare_util import face_distance
from utils.db import FaceDatabaseManager
from utils.face_util import face_embedding, face_detection
from app import create_app
import cv2

app = create_app()
flask_cors.CORS(app)  # 在应用中启用 CORS

@app.route('/add_face', methods=['POST'])
def add_face():
    # 解析请求体中的JSON数据
    data = request.json
    image_base64 = data['image']
    name = data['name']
    group = data['group']

    # 将base64编码的图片解码成bytes类型
    image_data = base64.b64decode(image_base64)
    # 将bytes编码的图片解码成np.ndarray类型
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    # 提取图片中的人脸特征向量
    feature = face_embedding(img)

    # 创建 FaceDatabaseManager 的实例
    face_database_manager = FaceDatabaseManager()
    # 将人脸信息保存到数据库中，并获得新增人脸的ID
    face_id = face_database_manager.add_face(name, group, feature.tobytes(), image_base64)

    # 将人脸特征向量保存到缓存中
    RedisManager.set(FACE_KEY_INDEX + str(face_id), feature.tobytes())

    # 返回JSON响应
    return jsonify({
        'success': True,
        'face_id': face_id
    })


@app.route('/face_recognition', methods=['POST'])
def face_recognition():
    # 获取图片
    image_b64 = request.form['image']
    image_bytes = base64.b64decode(image_b64)

    # 将bytes编码的图片解码成np.ndarray类型
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # 提取图片特征向量
    feature = face_embedding(img)

    # 遍历 Redis 中所有的人脸特征向量，计算相似度
    face_keys = RedisManager.get_all_face_keys()
    distances = []
    for face_key in face_keys:
        face_id = face_key[len(FACE_KEY_INDEX):]
        face_vector = RedisManager.get(face_key)
        face_to_compare = np.frombuffer(face_vector, dtype=np.float64)
        distance = face_distance(feature, face_to_compare)
        distances.append((face_id, distance))
    if len(distances) == 0:
        return jsonify(success=False, message='未找到匹配的人脸', data=[])

    # 根据相似度排序，找到最相似的人脸
    distances.sort(key=lambda x: x[1])
    face_id = distances[0][0]

    # 创建 FaceDatabaseManager 的实例
    face_database_manager = FaceDatabaseManager()

    # 从数据库中获取人脸信息并返回
    name, group, feature = face_database_manager.get_face_by_id(face_id)
    if name is None:
        return jsonify(success=False, message='未找到匹配的人脸', data=[])
    return jsonify(success=True, message='识别成功', data=[{
        'id': str(face_id),
        'name': name,
        'group': group
    }])

@app.route('/api/face_database')
@flask_cors.cross_origin()
def face_database():
    # 获取分页参数
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    # 获取查询参数
    name = request.args.get('name')
    group = request.args.get('group')

    # 创建 FaceDatabaseManager 的实例
    face_database_manager = FaceDatabaseManager()
    if group == '':
        group = None
    if name == '':
        name = None
    # 从数据库中获取人脸信息并返回
    faces, total = face_database_manager.get_face_list(page, limit, name, group)

    last_page = (total + limit - 1) // limit

    # 组装响应数据
    result = {
        "code": 0,
        "msg": "",
        "data": {
            "total": total,
            "per_page": limit,
            "current_page": page,
            "last_page": last_page,
            "data": []
        }
    }
    for face in faces:
        result['data']['data'].append({
            'id': face.id,
            'name': face.name,
            'group': face.group,
            'created_time': face.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_time': face.updated_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_deleted': face.is_deleted,
            'face_base64': face.face_base64
        })
    return jsonify(result)

@app.route('/face_detection', methods=['POST'])
def face_detection_api():
    # 解析请求体中的JSON数据
    data = request.json
    image_base64 = data['image']
    # 将base64编码的图片解码成bytes对象
    image_bytes = base64.b64decode(image_base64)
    # 将bytes对象转换成numpy数组
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    # 检测人脸
    faces = face_detection(img)
    # 构建返回结果
    success = True if faces else False
    message = "No face detected!" if not faces else ""
    faces_np = np.array(faces)
    data = {"faces": faces_np.tolist()}
    # 返回响应结果
    return jsonify({"success": success, "message": message, "data": data})

@app.route('/api/face_database/<int:id>', methods=['PUT'])
def update_face(id):
    # 解析请求中的JSON数据
    data = request.json
    name = data.get('name')
    group = data.get('group')
    face_base64 = data.get('face_base64')

    # 如果传入了人脸图片数据，则提取人脸特征向量
    if face_base64 is not None:
        # 将base64编码的图片解码成bytes类型
        image_data = base64.b64decode(face_base64)
        # 将bytes编码的图片解码成np.ndarray类型
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        # 提取图片中的人脸特征向量
        feature = face_embedding(img)
    else:
        feature = None

    # 更新数据库中的人员信息
    face_database_manager = FaceDatabaseManager()
    success = face_database_manager.update_face(id, name, group, feature.tobytes() if feature is not None else None, face_base64)

    if success:
        # 如果更新成功，则更新人脸特征缓存
        if feature is not None:
            RedisManager.set(FACE_KEY_INDEX + str(id), feature.tobytes())
        else:
            RedisManager.delete(FACE_KEY_INDEX + str(id))
        return jsonify({
            'code': 0,
            'msg': ''
        })
    else:
        return jsonify({
            'code': -1,
            'msg': 'Update face failed'
        })


@app.route('/api/face_database/<int:id>', methods=['DELETE'])
def delete_face(id):
    # 创建 FaceDatabaseManager 的实例
    face_database_manager = FaceDatabaseManager()

    # 从数据库中删除人脸信息
    deleted = face_database_manager.delete_face(id)
    if not deleted:
        return jsonify(success=False, message='未找到指定的人脸信息', data=None), 200

    # 从缓存中删除人脸特征向量
    RedisManager.delete(FACE_KEY_INDEX + str(id))

    # 返回响应
    return jsonify(success=True, message='删除成功', data=None), 200

if __name__=="__main__":
    app.run(debug=True)