import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_NOTIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///products.db'
