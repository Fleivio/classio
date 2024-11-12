from mvc_flask import Router
from flask import *
from app.models import User, Token
from app.models import db

Router.post('/debug/add_user', 'debug#add_user')
Router.post('/debug/test', 'debug#test')
Router.post('/debug/login', 'debug#login')

Router.get('/debug/get_all_users', 'debug#get_all_users')
Router.get('/debug/get_user/<int:id>', 'debug#get_user_by_id')
Router.get('/debug/gen_token', 'debug#gen_token')
