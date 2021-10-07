import uuid
from datetime import timedelta
import jwt
from flask import jsonify, request, make_response
from flask_wtf.csrf import CSRFError, generate_csrf, validate_csrf
from conf import app, csrf, db
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


# todo à faire
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

# @app.before_request
# def check_csrf():
#     print('csrf protect')
#     csrf.protect()


# @app.after_request
# def set_xsrf_cookie(response):
#     print('after_request')
#     response.set_cookie('X-CSRFToken',
#                         generate_csrf(secret_key=app.config['WTF_CSRF_SECRET_KEY'], token_key=app.config['TOKEN_KEY']))
#     return response
