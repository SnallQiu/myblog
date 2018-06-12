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
    create_time = db.Column(db.DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S'))

    def __init__(self, user_id, title, status):
        self.user_id = user_id
        self.title = title
        self.status = status
        #self.create_time = datetime.fromtimestamp(time.time())
from markdown import markdown
import bleach
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(24), nullable=False)
    link = db.Column(db.String(60),nullable=False)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    vote = db.Column(db.Integer,default=0)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.fromtimestamp((time.time())))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    '''markdown
    https://blog.csdn.net/hyman_c/article/details/54426242
    '''
    @staticmethod
    def on_body_change(target, value, oldvalue, initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
            'h1', 'h2', 'h3', 'p'
        ]
        body = markdown(value, output_format='html')
        body = bleach.clean(body, tags=allowed_tags, strip=True)
        body = bleach.linkify(body)
        target.body_html = body

db.event.listen(Post.body,'set',Post.on_body_change)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False , unique=True)
    #password = db.Column(db.String(24), nullable=False)
    password_hash = db.Column(db.String(120),nullable=False)
    '''User 和 Post是一对多的关系，backref是表示在Post中新建一个属性author，关联的是Post中author_id外键关联的User对象
    '''
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    #role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(24),unique=True)
    default = db.Column(db.Boolean , default = False , index=True)
    permissions = db.Column(db.Integer)
    #users = db.relationship('User',backref='role',lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles={
            'User':(Permission.Follow | Permission.Comment | Permission.Write_Artiles , True),
            'Moderator':(Permission.Follow | Permission.Comment | Permission.Write_Artiles | Permission.Moderate_comments , False ),
            'Administrator':(0xff,False)

        }
        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

'''定义权限常量'''
class Permission:
    Follow = 0x01
    Comment = 0x02
    Write_Artiles = 0x04
    Moderate_comments = 0x08
    Administer = 0x80