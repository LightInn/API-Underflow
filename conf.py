import os
from datetime import timedelta

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
# app.config['WTF_CSRF_FIELD_NAME'] = os.getenv('WTF_CSRF_FIELD_NAME')
app.config['WTF_CSRF_CHECK_DEFAULT'] = os.getenv('WTF_CSRF_CHECK_DEFAULT')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SESSION_COOKIE_SECURE'] = False
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['WTF_CSRF_SSL_STRICT'] = False
# app.config['SESSION_COOKIE_DOMAIN'] = "localhost.local"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_COOKIE_SAMESITE'] = "None"

CSRF = False

csrf = None
if CSRF:
	csrf = CSRFProtect(app)
CORS(app)
db = SQLAlchemy(app)
