from typing import Dict, List, Union
import numpy as np
import cv2
from utils import align
from utils.align import pad_input_image, recover_pad_output
import json
import requests

FACE_DETECTION_API_URL = 'http://172.16.0.21:8501/v1/models/face/versions/3:predict'
FACE_EMBEDDING_API_URL = 'http://172.16.0.21:8501/v1/models/face/versions/2:predict'


def face_detection(img_raw: np.ndarray) -> List[Dict[str, Union[str, float]]]:
    """
    Detects faces in the input image and returns the aligned faces along with padding parameters.

    Parameters:
    img_raw (numpy.ndarray): The input image as a numpy array.

    Returns:
    List[Dict[str, Union[str, float]]]: A list of dictionaries containing the aligned faces and padding parameters.
    """
    img_height_raw, img_width_raw, _ = img_raw.shape
    img = cv2.resize(img_raw, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img, pad_params = pad_input_image(img, max_steps=max([8, 16, 32]))
    data = json.dumps({'instances': img[np.newaxis, ...].tolist()})
    res = requests.post(FACE_DETECTION_API_URL, data=data)
    json_data = res.json()
    outputs = recover_pad_output(np.array(json_data['predictions']), pad_params, score_th=0.85)
    faces = align.get_aligned_faces(img_raw, outputs, img_width_raw, img_height_raw)
    return faces


def face_embedding(img_raw: np.ndarray) -> np.ndarray:
    """
    Extracts features from a given face.

    Parameters:
    img_raw (numpy.ndarray): The input image as a numpy array.

    Returns:
    numpy.ndarray: The extracted features as a numpy array.
    """
    img_height_raw, img_width_raw, _ = img_raw.shape
    img = cv2.resize(img_raw, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img, pad_params = pad_input_image(img, max_steps=max([8, 16, 32]))
    data = json.dumps({'instances': img[np.newaxis, ...].tolist()})
    res = requests.post(FACE_DETECTION_API_URL, data=data)
    json_data = res.json()
    outputs = recover_pad_output(np.array(json_data['predictions']), pad_params, score_th=0.85)
    faces = align.get_aligned_faces(img_raw, outputs, img_width_raw, img_height_raw)

    embeddings = []
    for face in faces:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face = face - 127.5
        face = face * 0.0078125
        face = np.transpose(face, (2, 0, 1))
        data = json.dumps({'instances': face[np.newaxis, ...].tolist()})
        res = requests.post(FACE_EMBEDDING_API_URL, data=data)
        json_data = res.json()
        embeddings.append(json_data['predictions'][0])
    return np.array(embeddings)
