# -- coding: utf-8 --
# author: snall  time: 2018/4/30

from flask import Blueprint

main =  Blueprint('main',__name__)

from . import views