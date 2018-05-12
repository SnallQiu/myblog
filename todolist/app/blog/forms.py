# -- coding: utf-8 --
# author: snall  time: 2018/5/1

from flask_wtf import FlaskForm,Form
from wtforms import RadioField,StringField,SubmitField,SelectField,IntegerField,TextAreaField
from wtforms.validators import Regexp,DataRequired,Length

class Blog_items(Form):
    title = StringField('Set Your blog name!')
    body = TextAreaField("what's on your mind?", validators=[DataRequired()])
    #publish_time = StringField('publish_time',validators = [DataRequired()])
    #score = IntegerField('score',validators=[DataRequired()])
    submit = SubmitField('Submit')