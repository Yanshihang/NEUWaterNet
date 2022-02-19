
# Created by 闫世航 on 2021/10/11

# 配置文件
class Config:
    # SQLALCHEMY_DATABASE_URI =‘mysql + 驱动名 + ://用户名:用户密码@主机IP地址:端口号(port)/数据库名称’
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:cid418sh@127.0.0.1:3306/web_work'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = 'zizhou'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
