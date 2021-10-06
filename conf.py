from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
login_manager = LoginManager()
csrf = CSRFProtect()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:dbpassd@82.65.232.137:5432/scratchunderflow'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../API-Underflow/aaa.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'fc036e4bc6974f92bb6577ae886ae113'
app.config['WTF_CSRF_SECRET_KEY'] = 'csrf_secret_key'
app.config['WTF_CSRF_FIELD_NAME'] = 'X-CSRFToken'
app.config['WTF_CSRF_CHECK_DEFAULT'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True

CORS(app)
login_manager.init_app(app)
csrf.init_app(app)
db = SQLAlchemy(app)
