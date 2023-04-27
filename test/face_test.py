import json
import unittest
import base64

import requests as requests


class AddFaceTestCase(unittest.TestCase):
    def setUp(self):
        self.image_path = 'test_image.jpg'
        self.name = 'Test'
        self.group = 'TestGroup'

    def tearDown(self):
        pass

    def test_add_face(self):
        url = "http://localhost:5000/add_face"
        # 读取本地图片并转化为base64编码
        with open('/home/zoneyet/图片/test2.jpg', 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')
        # 构造POST请求的JSON数据
        json_data = {
            "name": "test_name",
            "group": "test_group",
            "image": img_base64
        }
        # 发送POST请求
        response = requests.post(url, json=json_data)
        # 检查响应状态码和JSON数据
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert isinstance(response.json()["face_id"], int)

    def test_face_recognition(self):
        # 构造 POST 请求
        url = 'http://localhost:5000/face_recognition'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        image_path = '/home/zoneyet/图片/test2.jpg'
        with open(image_path, 'rb') as f:
            image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        data = {'image': image_base64}

        # 发送请求
        response = requests.post(url, headers=headers, data=data)
        result = response.json()

        # 断言返回值
        assert result['success'] == True
        assert result['message'] == '识别成功'
        assert 'data' in result
        assert len(result['data']) == 1
        assert 'id' in result['data'][0]
        assert 'name' in result['data'][0]
        assert 'group' in result['data'][0]

    def test_face_detection_api(self):
        # 构建请求体
        data = {
            "image": image_to_base64("/home/zoneyet/图片/test2.jpg")
        }

        # 发送POST请求
        response = requests.post("http://localhost:5000/face_detection", json=data)

        # 解析响应结果
        response_data = response.json()

        # 断言结果
        self.assertTrue("success" in response_data)
        self.assertTrue("message" in response_data)
        self.assertTrue("data" in response_data)

    def test_get_face_list_with_valid_params(self):
        query_params = {
            'page': 1,
            'limit': 10,
            'name': 'John',
            'group': 'Team A'
        }
        response = requests.get('http://localhost:5000/api/face_database', params=query_params)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['code'], 0)
        self.assertEqual(response_data['data']['current_page'], 1)
        self.assertEqual(response_data['data']['per_page'], 10)
        self.assertIsNotNone(response_data['data']['data'])
        self.assertIsNotNone(response_data['data']['total'])
        self.assertIsNotNone(response_data['data']['last_page'])

    def test_update_face_with_face_data(self):
        base64 = image_to_base64("/home/zoneyet/图片/test2.jpg")
        data = {
            'name': 'John Doe',
            'group': 'Employees',
            'face_base64': base64
        }
        response = requests.put('http://localhost:5000/api/face_database/164', headers={'Content-Type': 'application/json'}, json=data)
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.text)
        self.assertEqual(json_data['code'], 0)
        self.assertEqual(json_data['msg'], '')

    def test_delete_face(self):
        # Delete the added face from database
        r = requests.delete('http://localhost:5000/api/face_database/' + str(164))

        # Verify response status code and message
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['message'], '删除成功')

        # Verify that the face is no longer in the database
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json()['message'], '未找到指定的人脸信息')
def image_to_base64(filepath):
    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')
if __name__ == '__main__':
    unittest.main()