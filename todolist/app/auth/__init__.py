# -- coding: utf-8 --
# author: snall  time: 2018/4/22
from flask import Blueprint

auth = Blueprint('auth',__name__)

from .view import login
