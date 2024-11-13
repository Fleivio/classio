import os

class Config:
    SECRET_KEY = 'uma-chave-secreta-dificil'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.path.dirname(__file__), "../app_database.sqlite")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_NAME = 'classio_token'