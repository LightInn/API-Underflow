from scheme import *
from security import *
from flask import request, Response
import re


@app.route("/populate/", methods=["GET"])
def populate():
    # new_user = User(id=uuid.uuid4(), alternative_id=uuid.uuid4(), first_name='Mathis', last_name='Gauthier',
    #                 email='mathis.gauthier@epsi.fr',
    #                 password=str.encode('123456'))
    # db.session.add(new_user)
    # db.session.commit()
    # new_class = Class(title='B1')
    # new_class2 = Class(title='B2')
    # db.session.add(new_class)
    # db.session.commit()
    # db.session.add(new_class2)
    # db.session.commit()
    owner = User.query.filter_by(email='mathis.gauthier@epsi.fr').first()
    # new_subject = Subject(title='PHP', validated=True, proposePar=owner)
    # new_subject2 = Subject(title='JS', validated=True, proposePar=owner)
    # db.session.add(new_subject)
    # db.session.commit()
    # db.session.add(new_subject2)
    # db.session.commit()
    subject = Subject.query.filter_by(title='PHP').first()
    subject2 = Subject.query.filter_by(title='JS').first()
    classe = Class.query.filter_by(title='B1').first()
    # new_proposition = Proposition(title='Besoin d\'aide en PHP', subject=subject,
    #                               date_butoir=(datetime.now(pytz.timezone('Europe/Paris')) + timedelta(weeks=1)),
    #                               classe=classe, owner=owner)
    # db.session.add(new_proposition)
    # db.session.commit()
    new_proposition = Proposition(title='Besoin d\'aide en JS', subject=subject2,
                                  date_butoir=(datetime.now(pytz.timezone('Europe/Paris')) + timedelta(weeks=1)),
                                  classe=classe, owner=owner)
    db.session.add(new_proposition)
    db.session.commit()
    proposition = Proposition.query.filter_by(id=1).first()
    # course = Course(title="Cours JS", description="Révision JS",
    #                 date_start=(datetime.now(pytz.timezone('Europe/Paris')) + timedelta(days=1)), classe=classe,
    #                 subject=subject2, owner=owner)
    # db.session.add(course)
    # db.session.commit()
    cours = Course.query.filter_by(id=1).first()
    # subscription = CourseSubscription(participant=owner, course=cours)
    # db.session.add(subscription)
    # db.session.commit()
    return Response(status=200)


# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return jsonify({
#         'error': e.description,
#     }), 401


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
    if re.search(r"@((epsi.fr)|(ecoles-wis.net))$", data['email']):
        check_user = User.query.filter_by(email=data['email']).first()
        if check_user is None:
            password = str.encode(data['password'])
            new_user = User(id=uuid.uuid4(), alternative_id=uuid.uuid4(), first_name=data['first_name'],
                            last_name=data['last_name'],
                            email=data['email'], password=password,
                            created_on=datetime.now(pytz.timezone('Europe/Paris')))
            db.session.add(new_user)
            db.session.commit()
            return Response(status=201)

    return jsonify({
        'error': 'Invalid email'
    }), 418


@app.route("/login/", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.verify_password(str.encode(data['password'])):
        token = jwt.encode(
            {'id': str(user.alternative_id),
             'exp': datetime.now(pytz.timezone('Europe/Paris')) + timedelta(minutes=30)},
            app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({
            'token': token
        }), 200
    return jsonify({
        'error': 'Wrong email or password'
    }), 401


# Endpoint to add a new subject.
@app.route("/subject/", methods=["POST"])
def add_subject():
    auth = verify_authentication(request.headers)
    if auth:
        data = request.get_json()
        new_subject = Subject(title=data['title'], proposePar=auth)
        db.session.add(new_subject)
        db.session.commit()
        return Response(status=201)
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all subjects.
@app.route("/subjects/", methods=["GET"])
def get_subjects():
    auth = verify_authentication(request.headers)
    if auth:
        subjects = Subject.query.all()
        return jsonify(subjects), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to logout an user, by changing his alternative_id to invalidate every JWT.
@app.route("/logout/", methods=["POST"])
def logout():
    auth = verify_authentication(request.headers)
    if auth:
        auth.alternative_id = uuid.uuid4()
        db.session.commit()
    return Response(status=200)


# Endpoint to get a list of all courses
@app.route("/courses/")
def courses():
    auth = verify_authentication(request.headers)
    if auth:
        courses = Course.query.filter_by(ended=False).all()
        return jsonify(courses), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all propositions of courses
@app.route("/propositions/", methods=["GET"])
def get_propositions():
    auth = verify_authentication(request.headers)
    if auth:
        # TODO sélectionner que les champs utiles (Proposition.id, Proposition.title, Proposition.date_butoir,
        #  Proposition.subject.id, Proposition.subject.title, Proposition.classe.id, Proposition.classe.title)
        propositions = Proposition.query.all()
        return jsonify(propositions), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


@app.route("/proposition/", methods=["POST"])
def add_proposition():
    auth = verify_authentication(request.headers)
    if auth:
        data = request.get_json()
        check_subject = Subject.query.filter_by(id=data.subject.id).first()
        if not check_subject:
            new_subject = Subject(title=data.subject.title, proposePar=auth)
            db.session.add(new_subject)
            db.session.commit()
            subject = Subject.query.filter_by(title=data.subject.title).first()
            data.subject = subject
        classe = Class.query.filter_by(id=data.classe.id).first()
        new_proposal = Proposition(title=data.title, date_butoir=data.date_butoir, classe=classe, owner=auth,
                                   subject=data.subject)
        db.session.add(new_proposal)
        db.session.commit()
        return Response(status=201)
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all the participants from a course
@app.route("/course/<course_id>/participants/")
def course_participants(course_id):
    auth = verify_authentication(request.headers)
    if auth:

        participants = User.query.filter(CourseSubscription.participant).filter_by(ended=False).all()
        participants = User.query.filter_by()
        return Response(status=200)
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


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
    auth = verify_authentication(request.headers)
    if auth:
        # do something
        return jsonify(), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all classes
@app.route("/classes/")
def classes():
    auth = verify_authentication(request.headers)
    if auth:
        classes = Class.query.all()
        return jsonify(classes), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all students from a class
@app.route("/class/<int:class_id>/students/")
def class_students(class_id):
    auth = verify_authentication(request.headers)
    if auth:
        # do something
        return Response(status=200)
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get the profil of specific user
@app.route("/user/profile/", methods=['GET'])
def get_user_profile():
    auth = verify_authentication(request.headers)
    if auth:
        user = User.query.filter_by(alternative_id=auth.alternative_id).first()
        return jsonify(user), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get all comments of specific user
@app.route("/user/comments/", methods=['GET'])
def user_comments():
    auth = verify_authentication(request.headers)
    if auth:
        comments = Comment.query.filter_by(owner=auth).all()
        return jsonify(comments), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get all subscriptions of a specific user
@app.route("/user/subscriptions/", methods=['GET'])
def user_subscriptions():
    auth = verify_authentication(request.headers)
    if auth:
        subscriptions = Course.query.filter(CourseSubscription.participant == auth).filter_by(ended=False).all()
        return jsonify(subscriptions)
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to subscribe or unsubscribe to a course depend on previous subscription or not
@app.route("/subscription/", methods=['POST'])
def subscribe():
    auth = verify_authentication(request.headers)
    if auth:
        data = request.get_json()
        subscription = CourseSubscription.query.filter_by(course_id=data.course_id, participant_id=auth.id).first()
        if subscription:
            db.session.delete(subscription)
            db.session.commit()
        else:
            new_subscription = CourseSubscription(participant=auth, course=data.course_id)
            db.session.add(new_subscription)
            db.session.commit()
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401
