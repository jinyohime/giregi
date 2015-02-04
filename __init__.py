from flask import Flask
from flask.ext.bcrypt import Bcrypt

app=Flask(__name__)
app.secret_key='\xe98\xd4[\xd4\x01\xd9)\xfb\x11F\xb6\xe8\xd2\xed\xc2\x94\xc8\xf4W5\xd8;\x89'
app.config['SQLALCHEMY_ECHO']=True
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://ubuntu:1234@localhost/ubuntu'
bcrypt=Bcrypt(app)
#WARNING : change p.rogramming to your psql password


from controller import *

