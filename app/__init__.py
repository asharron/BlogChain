#Initalizes the app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os 
from config import basedir
from steem import Steem
from flask.ext.misaka import Misaka


app = Flask(__name__)
mail = Mail(app)
app.config.from_object('config')
db = SQLAlchemy(app)
app.secret_key = "secret"
Misaka(app)
node = ['https://steemd.steemit.com']
s = Steem(node)

from app import views, models
