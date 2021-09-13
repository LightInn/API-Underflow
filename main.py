from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:dbpassd@82.65.232.137:5432/scratchunderflow'
db = SQLAlchemy(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80), unique=False, nullable=False)
	last_name = db.Column(db.String(80), unique=False, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(120), unique=False, nullable=False)

	class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
	classe = db.relationship('Class', backref=db.backref('users', lazy=True))

	def __repr__(self):
		return '<User %r>' % self.username


class Class(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)

	def __repr__(self):
		return '<Post %r>' % self.title


class Proposition(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	description = db.Column(db.Text, nullable=False)
	date_proposition = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
	classe = db.relationship('Class', backref=db.backref('users', lazy=True))

	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
	subject = db.relationship('Subject', backref=db.backref('propositions', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


class Subject(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False)

	def __repr__(self):
		return '<Category %r>' % self.title


class Tutorial(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	description = db.Column(db.Text, nullable=False)
	date_proposition = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
	classe = db.relationship('Class', backref=db.backref('users', lazy=True))

	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
	subject = db.relationship('Subject', backref=db.backref('propositions', lazy=True))

	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	owner = db.relationship('User', backref=db.backref('tutorials_owner', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


class TutorialSubscription(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	confirmed = db.Column(db.Boolean, default=False, nullable=False)

	participant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	participant = db.relationship('User', backref=db.backref('tutorial_participation', lazy=True))

	tutorial_id = db.Column(db.Integer, db.ForeignKey('tutorial.id'), nullable=False)
	tutorial = db.relationship('Tutorial', backref=db.backref('participant', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


class Thread(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Boolean, default=False, nullable=False)

	participant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	participant = db.relationship('User', backref=db.backref('tutorial_participation', lazy=True))

	tutorial_id = db.Column(db.Integer, db.ForeignKey('tutorial.id'), nullable=False)
	tutorial = db.relationship('Tutorial', backref=db.backref('participant', lazy=True))

	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	owner = db.relationship('User', backref=db.backref('threads', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


class CommentVote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	vote = db.Column(db.Boolean, default=False, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
	comment = db.relationship('Comment', backref=db.backref('votes', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Boolean, default=False, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	owner = db.relationship('User', backref=db.backref('comments', lazy=True))

	parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
	parent_comment = db.relationship('Comment', backref=db.backref('comments', lazy=True))

	thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=True)
	thread = db.relationship('Thread', backref=db.backref('comments', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


class File(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Boolean, default=False, nullable=False)

	thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
	thread = db.relationship('Thread', backref=db.backref('files', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


db.create_all()


# Endpoint to test the API connectivity
@app.route("/api/test/")
def test():
	return jsonify({
		'status': 'ok'
	})


# Endpoint to get a list of all users
@app.route("/api/users/")
def users():
	return "Users"


# Endpoint to get a list of all courses
@app.route("/api/courses/")
def courses():
	return "Courses"


# Endpoint to get a list of all proposals of courses
@app.route("/api/proposals/")
def proposals():
	return "Proposals"


# Endpoint to get a list of all the participants from a course
@app.route("/api/course/<course_id>/participants/")
def course_participants(course_id):
	return "....."


# Endpoint to get a list of all threads
@app.route("/api/threads/")
def threads():
	return "Threads"


# Endpoint to get a list of all comments from a thread
@app.route("/api/thread/<thread_id>/comments/")
def thread_comments(thread_id):
	return "comments"


# Endpoint to get a list of all classes
@app.route("/api/classes/")
def classes():
	return "classes"


# Endpoint to get a list of all students from a class
@app.route("/api/class/<class_id>/students")
def class_students(class_id):
	return "students"


# Endpoint to get the profil of specific user
@app.route("/api/user/<user_id>/")
def user(user_id):
	return "user"


# Endpoint to get all comments of specific user
@app.route("/api/user/<user_id>/comments/")
def user_comments(user_id):
	return "comments of user"


if __name__ == "__main__":
	app.run(debug=True)
