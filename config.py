import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'uma-chave-secreta-dificil'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "app_database.sqlite")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False