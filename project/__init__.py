
# Created by 闫世航 on 2021/10/11

from flask import Flask

import settings
from project.model import db
from project.view import user_bp
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings.DevelopmentConfig)
    db.init_app(app=app)        # 初始化数据库
    Bootstrap(app)
    # bootstrap.init_app(app=app)
    app.register_blueprint(user_bp)     # 注册蓝图

    return app
