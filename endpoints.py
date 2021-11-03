import re
import cgi

import sqlalchemy
from flask import request, Response
from sqlalchemy import text
from scheme import *
from security import *


# Endpoint to give csrf-token before 'POST', 'PUT', 'PATCH', 'DELETE' methods, to avoid CSRF attacks
@app.route("/csrf-token/", methods=["GET"])
def csrf():
    csrf_token = "None"
    if bool(strtobool(os.getenv('ENABLE_CSRF'))):
        csrf_token = generate_csrf(secret_key=app.config['WTF_CSRF_SECRET_KEY'], token_key="csrf_token")

    return jsonify({
        'X-CSRF-Token': csrf_token
    })


# Endpoint to test mail
@app.route("/test-mail/", methods=["GET"])
def testmail():
    msg = Message('Confirmation de mail - Scratch Underflow', sender='noreply@scratchunderflow.fr',
                  recipients=['andy.cinquin@epsi.fr'])
    token = s.dumps('andy.cinquin@epsi.fr', salt=os.getenv('MAIL_SALT'))
    nom = 'andy.cinquin@epsi.fr'.split('@')[0]
    url = 'http://localhost:4200/' + 'confirmation-mail/' + token
    msg.html = "<div style='overflow: hidden;'><font size='-1'><u></u> <div style='margin:0;padding:10px 0' bgcolor='#ffffff' marginwidth='0' marginheight='0'> <br><table border='0' width='100%' height='100%' cellpadding='0' cellspacing='0' bgcolor='#ffffff'> <tbody><tr> <td align='center' valign='top' bgcolor='#ffffff' style='background-color:#ffffff'> <table border='0' width='600' cellpadding='0' cellspacing='0' bgcolor='#ffffff'> <tbody><tr> <td bgcolor='#ffffff' style='background-color:#ffffff;padding-left:30px;padding-right:30px;font-size:14px;line-height:20px;font-family:Helvetica,sans-serif;color:#333'> <div style='text-align:center;margin-bottom:10px;margin-top:20px'> <a href='https://scratchunderflow.fr/' target='_blank' ><img alt=' ' height='60' width='250' style='height:60px;width:250px' src='https://scratchunderflow.fr/assets/images/svg/ecureuil-right.svg'></a> </div>Bonjour " + nom + ", <br><br><strong>Je te souhaites la bienvenue sur Scratch Underflow ! :)</strong> <br><br>Pour activer ton compte, il faut vérifier ton email en cliquant sur ce bouton : <div style='text-align:center'><br><br><a style='display:inline-block;text-transform:uppercase;font-size:20px;line-height:20px;text-decoration:none;padding:10px;color:#fff;background:#6F93FF;margin:auto' href='" + url + "' target='_blank'>Valider mon email</a><br><br></div>Si le bouton ne fonctionne pas, copiez/collez ce lien dans votre navigateur:<br><br><a style='font-style:italic;color:#627BDF' href='" + url + "' target='_blank' >" + url + "</a><br><br>Très bonne journée ! ♥ <br><font color='#888888'> <strong>L'équipe Scratch Underflow</strong> <br></font><br><em style='font-style:italic;color:#aaa'>PS: Si vous n'avez pas demandé à créer de compte sur Scratch Underflow, ignorez simplement cet email.</em> <br><br></td></tr></tbody></table> </td></tr></tbody></table><br><br></div></font></div>"
    mail.send(msg)
    return jsonify({
        'status': 'token link validation sent ! - {}'.format('andy.cinquin@epsi.fr')
    }), 200


# Endpoint to send the mail confirmation
@app.route("/confirmation-mail/", methods=["POST"])
def mailto():
    data = request.get_json()
    if re.search(r"@((epsi.fr)|(ecoles-wis.net))$", data['email']):
        msg = Message('Confirmation de mail - Scratch Underflow', sender='noreply@scratchunderflow.fr',
                      recipients=[data['email']])
        token = s.dumps(data['email'], salt=os.getenv('MAIL_SALT'))
        nom = data['email'].split('@')[0]
        url = 'http://localhost:4200/' + 'confirmation-mail/' + token
        msg.html = "<div style='overflow: hidden;'><font size='-1'><u></u> <div style='margin:0;padding:10px 0' bgcolor='#ffffff' marginwidth='0' marginheight='0'> <br><table border='0' width='100%' height='100%' cellpadding='0' cellspacing='0' bgcolor='#ffffff'> <tbody><tr> <td align='center' valign='top' bgcolor='#ffffff' style='background-color:#ffffff'> <table border='0' width='600' cellpadding='0' cellspacing='0' bgcolor='#ffffff'> <tbody><tr> <td bgcolor='#ffffff' style='background-color:#ffffff;padding-left:30px;padding-right:30px;font-size:14px;line-height:20px;font-family:Helvetica,sans-serif;color:#333'> <div style='text-align:center;margin-bottom:10px;margin-top:20px'> <a href='https://scratchunderflow.fr/' target='_blank' ><img alt=' ' height='60' width='250' style='height:60px;width:250px' src='https://scratchunderflow.fr/assets/images/svg/ecureuil-right.svg'></a> </div>Bonjour " + nom + ", <br><br><strong>Je te souhaites la bienvenue sur Scratch Underflow ! :)</strong> <br><br>Pour activer ton compte, il faut vérifier ton email en cliquant sur ce bouton : <div style='text-align:center'><br><br><a style='display:inline-block;text-transform:uppercase;font-size:12px;line-height:20px;text-decoration:none;padding:10px;color:#fff;background:#6F93FF;margin:auto' href='" + url + "' target='_blank'>Valider mon email</a><br><br></div>Si le bouton ne fonctionne pas, copiez/collez ce lien dans votre navigateur:<br><br><a style='font-style:italic;color:#627BDF' href='" + url + "' target='_blank' >" + url + "</a><br><br>Très bonne journée ! ♥ <br><font color='#888888'> <strong>L'équipe Scratch Underflow</strong> <br></font><br><em style='font-style:italic;color:#aaa'>PS: Si vous n'avez pas demandé à créer de compte sur Scratch Underflow, ignorez simplement cet email.</em> <br><br></td></tr></tbody></table> </td></tr></tbody></table><br><br></div></font></div>"
        mail.send(msg)
        return jsonify({
            'status': 'token link validation sent ! - {}'.format(data['email'])
        }), 200


# Endpoint to confirm the token
@app.route("/confirmation-mail/<token>", methods=["GET"])
def confirm_email(token):
    try:
        email = s.loads(token, salt=os.getenv('MAIL_SALT'), max_age=60)
    except SignatureExpired:
        return jsonify({
            'status': 'token expired'
        }), 401
    check_user = User.query.filter_by(email=email).first()
    if check_user:
        check_user.activated = True
        db.session.add(check_user)
        db.session.commit()
        token = jwt.encode(
            {'id': str(check_user.alternative_id), 'admin': check_user.admin,
             'exp': datetime.now(pytz.timezone('Europe/Paris')) + timedelta(hours=24)},
            app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({
            'token': token
        }), 200
    return jsonify({
        'status': 'user does not exist'
    }), 401


# Endpoint to test the API connectivity
@app.route("/test/", methods=['GET'])
def test():
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401
    return Response(status=200)


@app.route("/register/", methods=['POST'])
def register():
    data = request.get_json()
    if re.search(r"@((epsi.fr)|(ecoles-wis.net))$", data['email']):
        check_user = User.query.filter_by(email=data['email']).first()
        if check_user is None:
            password = str.encode(data['password'])
            new_user = User(id=uuid.uuid4(), alternative_id=uuid.uuid4(), first_name=data['first_name'].capitalize(),
                            last_name=data['last_name'].upper(),
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
        if user.activated:
            token = jwt.encode(
                {'id': str(user.alternative_id), 'admin': user.admin,
                 'exp': datetime.now(pytz.timezone('Europe/Paris')) + timedelta(hours=24)},
                app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({
                'token': token
            }), 200
        else:
            return jsonify({
                'error': "The account isn't activated !",
                'not_activated': True
            }), 401
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
    return Response(status=418)


# Endpoint to get a list of all courses
@app.route("/courses/", methods=['GET'])
def get_courses():
    auth = verify_authentication(request.headers)
    if auth:
        with db.session.no_autoflush:
            courses = Course.query.filter_by(ended=False).all()
            for course in courses:
                if course.owner.email:
                    delattr(course.owner, 'email')
                if course.owner.admin or course.owner.admin is not None:
                    delattr(course.owner, 'admin')
                if course.owner.activated or course.owner.activated is not None:
                    delattr(course.owner, 'activated')
                if course.owner.last_login:
                    delattr(course.owner, 'last_login')
                if course.owner.created_on:
                    delattr(course.owner, 'created_on')
                if course.subject.proposePar:
                    delattr(course.subject, 'proposePar')
            return jsonify(courses), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all courses without the ones created by the logged users
@app.route("/user/available_courses/", methods=['GET'])
def get_available_courses():
    auth = verify_authentication(request.headers)
    if auth:
        with db.session.no_autoflush:
            courses = Course.query.filter(Course.ended == False, Course.owner != auth).all()
            for course in courses:
                if course.owner.email:
                    delattr(course.owner, 'email')
                if course.owner.admin or course.owner.admin is not None:
                    delattr(course.owner, 'admin')
                if course.owner.activated or course.owner.activated is not None:
                    delattr(course.owner, 'activated')
                if course.owner.last_login:
                    delattr(course.owner, 'last_login')
                if course.owner.created_on:
                    delattr(course.owner, 'created_on')
                if course.subject.proposePar:
                    delattr(course.subject, 'proposePar')
            return jsonify(courses), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all courses of current logged user
@app.route("/user/courses/", methods=['GET'])
def get_owner_courses():
    auth = verify_authentication(request.headers)
    if auth:
        with db.session.no_autoflush:
            courses = Course.query.filter_by(ended=False, owner=auth).all()
            for course in courses:
                if course.owner.email:
                    delattr(course.owner, 'email')
                if course.owner.admin or course.owner.admin is not None:
                    delattr(course.owner, 'admin')
                if course.owner.activated or course.owner.activated is not None:
                    delattr(course.owner, 'activated')
                if course.owner.last_login:
                    delattr(course.owner, 'last_login')
                if course.owner.created_on:
                    delattr(course.owner, 'created_on')
                if course.subject.proposePar:
                    delattr(course.subject, 'proposePar')
            return jsonify(courses), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to create a new Course
@app.route("/course/", methods=['POST'])
def add_course():
    auth = verify_authentication(request.headers)
    if auth:
        data = request.get_json()
        check_subject = Subject.query.filter_by(id=int(data['subject']['id'])).first()
        if not check_subject:
            new_subject = Subject(title=data['subject']['title'], proposePar=auth)
            db.session.add(new_subject)
            db.session.commit()
            check_subject = Subject.query.filter_by(title=data['subject']['title']).first()
        classe = Class.query.filter_by(id=int(data['classe']['id'])).first()
        new_course = Course(title=data['title'], classe=classe,
                            date_start=datetime.strptime(data['date_start'], '%Y-%m-%dT%H:%M'),
                            description=data['description'], owner=auth, room=data['room'], subject=check_subject)
        db.session.add(new_course)
        db.session.commit()
        if data['proposition_id'] is not None:
            proposition = Proposition.query.filter_by(id=data['proposition_id']).first()
            if proposition:
                db.session.delete(proposition)
                db.session.commit()
        return Response(status=201)
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to end a course
@app.route("/course/<int:course_id>/cloture/", methods=['POST'])
def cloture_course(course_id):
    auth = verify_authentication(request.headers)
    if auth:
        course = Course.query.filter_by(id=course_id, ended=False).first()
        if course and course.owner == auth:
            course.ended = True
            db.session.add(course)
            db.session.commit()
            return Response(status=200)
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to change the attendance status of a participant
@app.route("/course/<int:course_id>/user_attendance/", methods=["PATCH"])
def toggle_attendance_status(course_id):
    auth = verify_authentication(request.headers)
    if auth:
        course = Course.query.filter_by(id=course_id, ended=False).first()
        if course and course.owner == auth:
            data = request.get_json()
            course_subscription = CourseSubscription.query.filter_by(course=course).filter(
                User.email == data['email']).join(User).first()
            if course_subscription:
                course_subscription.present = not course_subscription.present
                db.session.add(course_subscription)
                db.session.commit()
                return jsonify({
                    "present": course_subscription.present
                }), 200
            return Response(status=418)
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all propositions of courses
@app.route("/propositions/", methods=["GET"])
def get_propositions():
    auth = verify_authentication(request.headers)
    if auth:
        with db.session.no_autoflush:
            propositions = Proposition.query.all()
            for proposition in propositions:
                if proposition.subject.proposePar:
                    delattr(proposition.subject, 'proposePar')
                if proposition.owner:
                    delattr(proposition, 'owner')
            return jsonify(propositions), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to add a proposition
@app.route("/proposition/", methods=["POST"])
def add_proposition():
    auth = verify_authentication(request.headers)
    if auth:
        data = request.get_json()
        check_subject = Subject.query.filter_by(id=int(data['subject']['id'])).first()
        if not check_subject:
            new_subject = Subject(title=data['subject']['title'], proposePar=auth)
            db.session.add(new_subject)
            db.session.commit()
            check_subject = Subject.query.filter_by(title=data['subject']['title']).first()
        classe = Class.query.filter_by(id=int(data['classe']['id'])).first()
        new_proposal = Proposition(title=data['title'],
                                   date_butoir=datetime.strptime(data['date_butoir'], '%Y-%m-%dT%H:%M'),
                                   classe=classe, owner=auth,
                                   subject=check_subject)
        db.session.add(new_proposal)
        db.session.commit()
        return Response(status=201)
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all the participants from a course
@app.route("/course/<int:course_id>/participants/", methods=['GET'])
def course_participants(course_id):
    auth = verify_authentication(request.headers)
    if auth:
        with db.session.no_autoflush:
            sql = text(
                "SELECT u.first_name as first_name, u.last_name as last_name, u.email as email, cs.present as present "
                "FROM user u "
                "JOIN course_subscription cs on u.id = cs.participant_id "
                "JOIN course c on c.id = cs.course_id WHERE c.id = :course_id AND c.ended = false").params(
                course_id=course_id)
            result = db.engine.execute(sql)
            rows = result.fetchall()
            data = []
            for row in rows:
                data.append({
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'present': row['present']
                })
            return jsonify(data), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all threads
@app.route("/threads/", methods=['GET'])
def get_threads():
    if not verify_authentication(request.headers):
        return jsonify({
            'status': 'invalid token'
        }), 401

    return "Threads"


# Endpoint to get a list of all comments from a thread
@app.route("/thread/<thread_id>/comments/", methods=['GET'])
def get_thread_comments(thread_id):
    auth = verify_authentication(request.headers)
    if auth:
        # do something
        return jsonify(), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all classes
@app.route("/classes/", methods=['GET'])
def get_classes():
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


# Endpoint to modify the profile of the logged users
@app.route("/user/profile/edit/", methods=['PATCH'])
def edit_user():
    auth = verify_authentication(request.headers)
    if auth:
        data = request.get_json()
        user = User.query.filter_by(alternative_id=auth.alternative_id).first()
        user.last_name = data['last_name'].upper()
        user.first_name = data['first_name'].capitalize()
        user.class_id = data['class_id']
        db.session.add(user)
        db.session.commit()
        return Response(status=200)
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to change password
@app.route("/user/profile/change_password/", methods=['PATCH'])
def change_password():
    auth = verify_authentication(request.headers)
    if auth:
        data = request.get_json()
        user = User.query.filter_by(alternative_id=auth.alternative_id).first()
        if user.verify_password(str.encode(data['old_password'])):
            if data['new_password'] == data['confirm_new_password'] and data['new_password'] != data['old_password']:
                user.password = str.encode(data['new_password'])
                user.alternative_id = uuid.uuid4()
                db.session.add(user)
                db.session.commit()
                return Response(status=200)
            else:
                return jsonify({
                    'status': 'New password must match the confirm new password, and new password can not be the same as old password'
                }), 406
        else:
            return jsonify({
                'status': 'invalid password'
            }), 403
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
        with db.session.no_autoflush:
            courses = Course.query.filter_by(ended=False).filter(CourseSubscription.participant_id == auth.id).join(
                CourseSubscription).all()
            for course in courses:
                if course.owner.email:
                    delattr(course.owner, 'email')
                if course.owner.admin or course.owner.admin is not None:
                    delattr(course.owner, 'admin')
                if course.owner.activated or course.owner.activated is not None:
                    delattr(course.owner, 'activated')
                if course.owner.last_login:
                    delattr(course.owner, 'last_login')
                if course.owner.created_on:
                    delattr(course.owner, 'created_on')
                if course.subject.proposePar:
                    delattr(course.subject, 'proposePar')
            return jsonify(courses), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to subscribe or unsubscribe to a course depend on previous subscription or not
@app.route("/subscription/", methods=['POST'])
def subscribe():
    auth = verify_authentication(request.headers)
    if auth:
        subscribed: bool
        data = request.get_json()
        subscription = CourseSubscription.query.filter_by(course_id=data['id'], participant=auth).first()
        if subscription:
            db.session.delete(subscription)
            db.session.commit()
            subscribed = False
        else:
            course = Course.query.filter_by(id=data['id']).first()
            new_subscription = CourseSubscription(participant=auth, course=course)
            db.session.add(new_subscription)
            db.session.commit()
            subscribed = True
        return jsonify({
            'subscribed': subscribed
        }), 200
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# ============================
# ENDPOINT ADMIN
# ============================
# Endpoint to add a classe
@app.route("/admin/classe/", methods=["POST"])
def add_classe():
    auth = verify_authentication(request.headers)
    if auth:
        if auth.admin:
            data = request.get_json()
            classe = Class(title=data["title"])
            db.session.add(classe)
            db.session.commit()
            return Response(status=200)
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to get a list of all users
@app.route("/admin/users/", methods=['GET'])
def get_users():
    auth = verify_authentication(request.headers)
    if auth:
        if auth.admin:
            users = User.query.all()
            return jsonify(users), 200
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to delete user
@app.route("/admin/delete_user/", methods=['DELETE'])
def delete_user():
    auth = verify_authentication(request.headers)
    if auth:
        if auth.admin:
            data = request.get_json()
            user_to_delete = User.query.filter_by(email=data['email']).first()
            if user_to_delete:
                db.session.delete(user_to_delete)
                db.session.commit()
                return Response(status=200)
            return Response(status=400)
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to update a subject
@app.route("/admin/update_subject/", methods=['PATCH'])
def update_subject():
    auth = verify_authentication(request.headers)
    if auth:
        if auth.admin:
            data = request.get_json()
            subject = Subject.query.filter_by(id=data['id']).first()
            if subject:
                subject.title = data['title']
                db.session.add(subject)
                db.session.commit()
                return Response(status=200)
            return Response(status=400)
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to delete a subject
@app.route("/admin/delete_subject/", methods=['DELETE'])
def delete_subject():
    auth = verify_authentication(request.headers)
    if auth:
        if auth.admin:
            data = request.get_json()
            subject = Subject.query.filter_by(id=data['id']).first()
            if subject:
                db.session.delete(subject)
                db.session.commit()
                return Response(status=200)
            return Response(status=400)
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to update a classe
@app.route("/admin/update_classe/", methods=['PATCH'])
def update_classe():
    auth = verify_authentication(request.headers)
    if auth:
        if auth.admin:
            data = request.get_json()
            classe = Class.query.filter_by(id=data['id']).first()
            if classe:
                classe.title = data['title']
                db.session.add(classe)
                db.session.commit()
                return Response(status=200)
            return Response(status=400)
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to delete a proposition
@app.route("/admin/delete_proposition/", methods=['DELETE'])
def delete_proposition():
    auth = verify_authentication(request.headers)
    if auth:
        if auth.admin:
            data = request.get_json()
            proposition = Proposition.query.filter_by(id=data['id']).first()
            if proposition:
                db.session.delete(proposition)
                db.session.commit()
                return Response(status=200)
            return Response(status=400)
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to delete a classe
@app.route("/admin/delete_classe/", methods=['DELETE'])
def delete_classe():
    auth = verify_authentication(request.headers)
    if auth:
        if auth.admin:
            data = request.get_json()
            classe = Class.query.filter_by(id=data['id']).first()
            if classe:
                db.session.delete(classe)
                db.session.commit()
                return Response(status=200)
            return Response(status=400)
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to update a course by
@app.route("/admin/update_course/", methods=['PATCH'])
def update_course():
    auth = verify_authentication(request.headers)
    if auth:
        if auth.admin:
            data = request.get_json()
            course = Course.query.filter_by(id=data['id']).first()
            if course:
                course.subject_id = data['subject_id']
                course.description = data['description']
                course.title = data['title']
                course.date_start = datetime.strptime(data['date_start'], '%Y-%m-%dT%H:%M')
                course.ended = data['ended']
                course.duration = data['duration']
                course.owner_id = data['owner_id']
                course.class_id = data['class_id']
                db.session.add(course)
                db.session.commit()
                return Response(status=200)
            return Response(status=400)
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401


# Endpoint to delete a course
@app.route("/admin/delete_course/", methods=['DELETE'])
def delete_course():
    auth = verify_authentication(request.headers)
    if auth:
        if auth.admin:
            data = request.get_json()
            course = Course.query.filter_by(id=data['id']).first()
            subscriptions = CourseSubscription.query.filter_by(course=course).all()
            if subscriptions:
                for subscription in subscriptions:
                    db.session.delete(subscription)
                    db.session.commit()
            if course:
                db.session.delete(course)
                db.session.commit()
                return Response(status=200)
            return Response(status=400)
        else:
            return jsonify({
                'status': 'Forbidden'
            }), 403
    else:
        return jsonify({
            'status': 'invalid token'
        }), 401
