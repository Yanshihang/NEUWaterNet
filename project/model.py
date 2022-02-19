
# Created by 闫世航 on 2021/10/11

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Students(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    dormitory = db.Column(db.String(8), nullable=False)
    isdelete = db.Column(db.Boolean, default=False)
    order = db.Column(db.Boolean, default=False)
    datetime = db.Column(db.DateTime, default=datetime.now)


class Worker(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    isdelete = db.Column(db.Boolean, default=False)
    application = db.Column(db.Boolean, default=False)  # 1(True)为申请通过可以正常登录，2(False)为等待申请通过


class Manager(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    isdelete = db.Column(db.Boolean, default=False)


class Notify(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.now)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, default=datetime.now)
