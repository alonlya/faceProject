from flask import Flask
from redis import Redis

from utils.db import FaceDatabaseManager

redis = Redis()
app = Flask(__name__)
def create_app():
    app = Flask(__name__)

    # 初始化数据库连接
    db_manager = FaceDatabaseManager()
    return app


if __name__=="__main__":
    create_app().run()