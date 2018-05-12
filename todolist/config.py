# -- coding: utf-8 --
# author: snall  time: 2018/4/22

class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'This is my key'

    @staticmethod
    def init_app(self):
        pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root@127.0.0.1/myblog"

config = {
    'development':DevelopmentConfig,
}