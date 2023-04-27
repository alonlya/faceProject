# 导入必要的模块
from flask import Flask
from flask_caching import Cache
import redis

# 导入配置
from config import CACHE_TYPE, CACHE_REDIS_HOST, CACHE_REDIS_PORT, CACHE_REDIS_PASSWORD, CACHE_REDIS_DB

FACE_KEY_INDEX = 'face_'

# 初始化Flask应用
app = Flask(__name__)

# 使用config.py中的配置初始化缓存
cache = Cache(app, config={
    'CACHE_TYPE': CACHE_TYPE,
    'CACHE_REDIS_HOST': CACHE_REDIS_HOST,
    'CACHE_REDIS_PORT': CACHE_REDIS_PORT,
    'CACHE_REDIS_PASSWORD': CACHE_REDIS_PASSWORD,
    'CACHE_REDIS_DB': CACHE_REDIS_DB,
})

# 初始化Redis连接
redis_pool = redis.ConnectionPool(
    host=CACHE_REDIS_HOST,
    port=CACHE_REDIS_PORT,
    password=CACHE_REDIS_PASSWORD,
    db=CACHE_REDIS_DB,
    decode_responses=False,
)
redis_conn = redis.Redis(connection_pool=redis_pool)

# Redis管理工具类
class RedisManager:
    @staticmethod
    def set(key, value, expire=None):
        """
        设置Redis中指定键的值
        :param key: 键
        :param value: 值
        :param expire: 过期时间（秒），默认为不过期
        :return: True（设置成功）或False（设置失败）
        """
        # try:
            # 设置键值
        redis_conn.set(key, value)
        # 如果设置了过期时间，则设置过期时间
        if expire is not None:
            redis_conn.expire(key, expire)
        return True
        # except:
        #     return False

    @staticmethod
    def get(key):
        """
        获取Redis中指定键的值
        :param key: 键
        :return: 键对应的值或None（获取失败）
        """
        # try:
        value = redis_conn.get(key)
        return value
        # except:
        #     return None

    @staticmethod
    def delete(key):
        """
        删除Redis中指定键的值
        :param key: 键
        :return: True（删除成功）或False（删除失败）
        """
        try:
            redis_conn.delete(key)
            return True
        except:
            return False

    @staticmethod
    def get_all_face_keys():
        """
        获取所有以'face_'为前缀的键
        :return: 返回一个列表，列表中包含所有以'face_'为前缀的键
        """
        try:
            keys = redis_conn.keys(FACE_KEY_INDEX + '*')
            return keys
        except:
            return []