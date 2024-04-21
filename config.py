import os

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   
