#!/usr/bin/python
#-*- coding: UTF-8 -*-
import time

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash , check_password_hash
from datetime import datetime
import time
class TodoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, title, status):
        self.user_id = user_id
        self.title = title
        self.status = status
        self.create_time = time.time()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(24), nullable=False)
    link = db.Column(db.String(60),nullable=False)
    body = db.Column(db.Text)
    vote = db.Column(db.Integer,default=0)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.fromtimestamp(time.time()))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    #password = db.Column(db.String(24), nullable=False)
    password_hash = db.Column(db.String(120),nullable=False)
    '''User 和 Post是一对多的关系，backref是表示在Post中新建一个属性author，关联的是Post中author_id外键关联的User对象
    '''
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


