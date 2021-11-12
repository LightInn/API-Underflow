import os
import uuid
from datetime import timedelta
from distutils.util import strtobool

import jwt
from flask import jsonify, request, make_response, session
from flask_wtf.csrf import CSRFError, generate_csrf, validate_csrf
from conf import app, db, csrf
import pytz
from scheme import User


def verify_authentication(headers):
    if headers.get('Authorization'):
        token_unverified = headers.get('Authorization')[7:]
        if validation_jwt(token_unverified):
            id_not_tested = (jwt.decode(token_unverified, key=app.config['SECRET_KEY'], algorithms='HS256'))['id']
            test_user_connexion = User.query.filter_by(alternative_id=id_not_tested).first()
            if test_user_connexion:
                return test_user_connexion
    return None


def logout_user(headers):
    token = headers.get('Authorization')[7:]
    id_to_change = (jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256'))['id']
    user = User.query.filter_by(alternative_id=id_to_change).first()
    user.alternative_id = uuid.uuid4()
    db.session.update(user)
    db.session.commit()
    return True


def validation_jwt(token_unverified):
    try:
        jwt.decode(token_unverified, key=app.config['SECRET_KEY'], algorithms='HS256')
    except:
        return False
    return True


def validation_jwt_password_reset(token_unverified):
    try:
        token_data = jwt.decode(token_unverified, key=app.config['RESET_PASSWORD_EMAIL'], algorithms='HS256')
        user = User.query.filter_by(email=token_data['email']).first()
        if user:
            if not str(user.alternative_id) == str(token_data['id']):
                raise ValueError
    except:
        return False
    return user


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    if bool(strtobool(os.getenv('ENABLE_CSRF'))):
        return jsonify({
            'error': e.description,
        }), 401


@app.before_request
def check_csrf():
    if bool(strtobool(os.getenv('ENABLE_CSRF'))):
        session.permanent = False
        csrf.protect()


@app.after_request
def handle_cookies(response):
    # resp = make_response("Session granted")
    # Set session cookie for a day
    # resp.set_cookie('test', 'SESSION_KEY', max_age=60 * 60 * 24, domain='localhost.local')
    # # Add CORS header to every response
    # response.headers["Access-Control-Allow-Origin"] = "*"
    # response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS,HEAD"
    # response.headers[
    # 	"Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, Authorization, set-cookies, " \
    #                                       "X-CSRFToken ,Set-Cookie, cookie"
    # response.headers["Access-Control-Allow-Credentials"] = True
    return response
