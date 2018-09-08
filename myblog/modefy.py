# -- coding: utf-8 --
# author: snall  time: 2018/5/1

from app import create_app,db
from app.models import User,Role

#if __name__ == '__main__':

app = create_app('development')
Role.insert_roles()