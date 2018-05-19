# -- coding: utf-8 --
# author: snall  time: 2018/4/22

class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
    SECRET_KEY = 'This is my key'
    BOOTSTRAP_SERVE_LOCAL = True

    @staticmethod
    def init_app(self):
        pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root@127.0.0.1/myblog"

config = {
    'development':DevelopmentConfig,
}