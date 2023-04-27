import os

import numpy as np
import pickle
def get_distance(emb1, emb2):
    diff = emb1 - emb2
    dist = np.sum(np.square(diff), axis=1)
    return dist

def get_candinator(emb, facebank):
    # pickle.load('/Users/destination/Downloads/starface-master/facebank.pkl')
    # pkls = open('/Users/destination/Downloads/starface-master/facebank.pkl', 'rb')  # 明星库
    pkls = os.listdir(facebank)
    if '.DS_Store' in pkls:
        pkls.remove('.DS_Store')
    for pkl in pkls:
        dists = []
        facepkl = open(os.path.join(facebank,pkl), 'rb')
        unmiddown = pickle.load(facepkl)
        dist = 999
        for faceemb in unmiddown[1]:
            tmpdist = get_distance(emb, faceemb)
            if tmpdist<dist:
                dist = tmpdist
        dists.append(dist)
    idx = np.argmin(dists)
    print(dists[idx])
    if dists[idx] < 0.9:
        candinator = pkls[idx]
        return candinator
    else:
        return None