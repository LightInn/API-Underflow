from conf import login_manager
from scheme import *
from security import *
from flask import request, Response, abort


@app.route("/populate/", methods=["GET"])
def populate():
    # new_user = User(id=uuid.uuid4(), first_name='Mathis', last_name='Gauthier', email='mathis.gauthier@epsi.fr',
    #                 password=str.encode('123456'))
    # db.session.add(new_user)
    # db.session.commit()
    # new_class = Class(title='B1')
    # new_class2 = Class(title='B2')
    # db.session.add(new_class)
    # db.session.commit()
    # db.session.add(new_class2)
    # db.session.commit()
    # new_subject = Subject(title='PHP')
    # new_subject2 = Subject(title='JS')
    # db.session.add(new_subject)
    # db.session.commit()
    # db.session.add(new_subject2)
    # db.session.commit()
    # subject = Subject.query.filter_by(title='PHP').first()
    # classe = Class.query.filter_by(title='B1').first()
    # new_proposition = Proposition(title='Besoin d\'aide en PHP', subject=subject,
    #                               date_butoir=(datetime.now(pytz.timezone('Europe/Paris')) + timedelta(weeks=1)),
    #                               classe=classe)
    # db.session.add(new_proposition)
    # db.session.commit()
    # proposition = Proposition.query.filter_by(id=1).first()
    # owner = User.query.filter_by(email="mathis.gauthier@epsi.fr").first()
    #
    # course = Course(title="Cours PHP", description="Révision PHP",
    #                 date_start=(datetime.now(pytz.timezone('Europe/Paris')) + timedelta(days=1)), classe=classe,
    #                 subject=subject, owner=owner)
    # db.session.add(course)
    # db.session.commit()
    return Response(status=200)


# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return jsonify({
#         'error': e.description,
#     }), 401


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# Endpoint to give csrf-token before 'POST', 'PUT', 'PATCH', 'DELETE' methods, to avoid CSRF attacks
@app.route("/csrf-token/", methods=["GET"])
def home():
    csrf_token = generate_csrf(secret_key=app.config['WTF_CSRF_SECRET_KEY'])
    return jsonify({
        'X-CSRF-Token': csrf_token
    })


# Endpoint to test the API connectivity
@app.route("/test/", methods=['GET'])
def test():
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401
    return Response(status=200)


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
        return Response(status=201)
    else:
        return jsonify({
            'error': 'Email already exists'
        }), 418


@app.route("/login/", methods=["POST"])
def login():
    data = request.get_json()
    print(request.headers)
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
            'token': token
        }), 200
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
