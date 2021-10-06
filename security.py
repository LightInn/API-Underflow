from datetime import timedelta
import jwt
from flask import jsonify, request, make_response
from flask_wtf.csrf import CSRFError, generate_csrf, validate_csrf
from conf import app, csrf
import pytz


def verify_authentication(headers):
    token_unverified = headers.get('Authorization')[7:]
    if not validation_jwt(token_unverified):
        return False
    else:
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
