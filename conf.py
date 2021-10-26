import os
from datetime import timedelta
from distutils.util import strtobool

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['ENV'] = os.getenv('ENV')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['WTF_CSRF_SECRET_KEY'] = os.getenv('WTF_CSRF_SECRET_KEY')
app.config['WTF_CSRF_CHECK_DEFAULT'] = bool(strtobool(os.getenv('WTF_CSRF_CHECK_DEFAULT')))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = bool(strtobool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')))
app.config['SESSION_COOKIE_SECURE'] = bool(strtobool(os.getenv('SESSION_COOKIE_SECURE')))
app.config['REMEMBER_COOKIE_SECURE'] = bool(strtobool(os.getenv('REMEMBER_COOKIE_SECURE')))
app.config['SESSION_COOKIE_HTTPONLY'] = bool(strtobool(os.getenv('SESSION_COOKIE_HTTPONLY')))
app.config['WTF_CSRF_SSL_STRICT'] = bool(strtobool(os.getenv('WTF_CSRF_SSL_STRICT')))
app.config['SESSION_COOKIE_DOMAIN'] = os.getenv('SESSION_COOKIE_DOMAIN')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=int(os.getenv('PERMANENT_SESSION_LIFETIME')))
app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE')

csrf = None
if bool(strtobool(os.getenv('ENABLE_CSRF'))):
    csrf = CSRFProtect(app)
CORS(app)
db = SQLAlchemy(app)
