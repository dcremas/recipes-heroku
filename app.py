import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

external_url = os.getenv('EXTERNAL_URL')
secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = external_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy()
db.init_app(app)

import routes, models
