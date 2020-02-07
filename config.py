import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flask-restplus'
    SQLALCHEMY_TRACK_MODIFICATIONS = False