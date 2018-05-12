# -- coding: utf-8 --
# author: snall  time: 2018/4/22

from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length,Regexp,EqualTo,ValidationError
from  ..models import User
from .. import db


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('登录')

class Register_User_Form(FlaskForm):
    #email = StringField('email',validators=[DataRequired(),Length(1,64)])
    username = StringField('用户名',validators=[DataRequired(),Length(1,64),
                                             Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                             'Username must have only letters,numbers,dots or underscores')])
    password = PasswordField('密码',validators=[DataRequired(),
                                              EqualTo('password2',message='Password must match')])
    password2 = PasswordField('确认密码',validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already in use .')



