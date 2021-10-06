from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:dbpassd@82.65.232.137:5432/scratchunderflow'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../API-Underflow/aaa.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'fc036e4bc6974f92bb6577ae886ae113'
app.config['TOKEN_KEY'] = 'a12b1c64bc584e7595e02830bd4bb981'
app.config['WTF_CSRF_SECRET_KEY'] = '2326321d3ad54bcfaafa33dd59cd2e26'
app.config['WTF_CSRF_CHECK_DEFAULT'] = True

csrf = CSRFProtect()
csrf.init_app(app)
db = SQLAlchemy(app)
