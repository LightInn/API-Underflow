from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:dbpassd@82.65.232.137:5432/scratchunderflow'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../API-Underflow/aaa.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'fc036e4bc6974f92bb6577ae886ae113'
app.config['TOKEN_KEY'] = 'test'
app.config['WTF_CSRF_SECRET_KEY '] = 'test'

# csrf = CSRFProtect()
# csrf.init_app(app)
db = SQLAlchemy(app)
