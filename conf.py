from dataclasses import dataclass
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:dbpassd@82.65.232.137:5432/scratchunderflow'
db = SQLAlchemy(app)