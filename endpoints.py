from conf import app
from scheme import *
import pytz
import conf
from security import *


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return jsonify({
        'error': e.description,
    }), 401


# Endpoint to test the API connectivity
@app.route("/test/", methods=['GET'])
def test():
    # csrf_token = generate_csrf(secret_key='test', token_key='test')
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    return jsonify({
        'status': 'OK'
    }), 200


# Endpoint to get a list of all users
@app.route("/users/", methods=['GET'])
def users():
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    users = User.query.all()
    return jsonify(users)


@app.route("/register/", methods=['POST'])
def register():
    data = request.get_json()
    check_user = User.query.filter_by(email=data['email']).first()
    if check_user is None:
        password = str.encode(data['password'])
        new_user = User(id=uuid.uuid4(), first_name=data['first_name'], last_name=data['last_name'],
                        email=data['email'], password=password, created_on=datetime.now(pytz.timezone('Europe/Paris')))
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user), 201
    else:
        return jsonify({
            'error': 'Email already exists'
        }), 418


@app.route("/login/", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user is None:
        return jsonify({
            'error': 'Wrong email or password'
        }), 401

    if user.verify_password(str.encode(data['password'])):
        token = jwt.encode(
            {'id': str(user.id), 'exp': datetime.now(pytz.timezone('Europe/Paris')) + timedelta(minutes=30)},
            app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({
            'token': 'Bearer ' + token
        })
    return jsonify({
        'error': 'Wrong email or password'
    }), 401


# Endpoint to get a list of all courses
@app.route("/courses/")
def courses():
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    return "Courses"


# Endpoint to get a list of all proposals of courses
@app.route("/proposals/")
def proposals():
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    return "Proposals"


# Endpoint to get a list of all the participants from a course
@app.route("/api/course/<course_id>/participants/")
def course_participants(course_id):
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    return "....."


# Endpoint to get a list of all threads
@app.route("/threads/")
def threads():
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    return "Threads"


# Endpoint to get a list of all comments from a thread
@app.route("/thread/<thread_id>/comments/")
def thread_comments(thread_id):
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    return "comments"


# Endpoint to get a list of all classes
@app.route("/classes/")
def classes():
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    return "classes"


# Endpoint to get a list of all students from a class
@app.route("/class/<class_id>/students")
def class_students(class_id):
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    return "students"


# Endpoint to get the profil of specific user
@app.route("/user/<string:user_id>/")
def user(user_id):
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    get_user = User.query.get(user_id)
    return jsonify(get_user)


# Endpoint to get all comments of specific user
@app.route("/user/<user_id>/comments/")
def user_comments(user_id):
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    return "comments of user"
