# -- coding: utf-8 --
# author: snall  time: 2018/5/1
from flask import Blueprint

blog = Blueprint('blog',__name__)

from . import views