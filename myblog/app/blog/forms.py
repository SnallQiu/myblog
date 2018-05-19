# -- coding: utf-8 --
# author: snall  time: 2018/5/1

from flask_wtf import FlaskForm,Form
from wtforms import RadioField,StringField,SubmitField,SelectField,IntegerField,TextAreaField
from wtforms.validators import Regexp,DataRequired,Length
from flask.ext.pagedown.fields import PageDownField
'''以下想自定义表高度 然后发现没什么卵用 先放着'''
from wtforms.widgets.core import TextArea
class MyTextArea(TextArea):
    def __init__(self,**kwargs):
        self.kwargs = kwargs

    def __call__(self, field, **kwargs):
        for arg in self.kwargs:
            if arg not in kwargs:
                kwargs[arg] = self.kwargs[arg]
        return super(MyTextArea,self).__call__(field,**kwargs)
class Blog_items(Form):
    title = StringField('Set Your blog name!')
    #body = TextAreaField("what's on your mind?", validators=[DataRequired()])
    '''markdown'''
    body =PageDownField("what's on your mind?",validators=[DataRequired(), Length(1, 9999, message='文章字数超出限制')])#,widget=MyTextArea(cols=1))
    #publish_time = StringField('publish_time',validators = [DataRequired()])
    #score = IntegerField('score',validators=[DataRequired()])
    submit = SubmitField('Submit')

class Show_blog(Form):
    body =PageDownField("",validators=[DataRequired(), Length(1, 9999, message='文章字数超出限制')])#,widget=MyTextArea(cols=1))

class Ensure_Delete(Form):
    status = RadioField('ENSURE DELETE!', validators=[DataRequired()],  choices=[('1', 'YES')])
    submit = SubmitField('COMMIT')
