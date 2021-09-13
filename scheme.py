import datetime
from dataclasses import dataclass
from conf import db


@dataclass
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	first_name = db.Column(db.String(80), unique=False, nullable=False)
	last_name = db.Column(db.String(80), unique=False, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(120), unique=False, nullable=False)

	class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=True)
	classe = db.relationship('Class', backref=db.backref('users', lazy=True))

	def __repr__(self):
		return '<User %r>' % self.username


@dataclass
class Class(db.Model):
	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	title = db.Column(db.String(80), nullable=False)

	def __repr__(self):
		return '<Post %r>' % self.title


@dataclass
class Proposition(db.Model):
	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	title = db.Column(db.String(80), nullable=False)
	description = db.Column(db.Text, nullable=False)
	date_proposition = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
	classe = db.relationship('Class', backref=db.backref('propositions', lazy=True))

	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
	subject = db.relationship('Subject', backref=db.backref('propositions', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


@dataclass
class Subject(db.Model):
	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	title = db.Column(db.String(50), nullable=False)

	def __repr__(self):
		return '<Category %r>' % self.title


@dataclass
class Tutorial(db.Model):
	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	title = db.Column(db.String(80), nullable=False)
	description = db.Column(db.Text, nullable=False)
	date_proposition = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
	classe = db.relationship('Class', backref=db.backref('tutorials', lazy=True))

	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
	subject = db.relationship('Subject', backref=db.backref('tutorials', lazy=True))

	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	owner = db.relationship('User', backref=db.backref('tutorials_owner', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


@dataclass
class TutorialSubscription(db.Model):
	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	confirmed = db.Column(db.Boolean, default=False, nullable=False)

	participant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	participant = db.relationship('User', backref=db.backref('tutorial_participation', lazy=True))

	tutorial_id = db.Column(db.Integer, db.ForeignKey('tutorial.id'), nullable=False)
	tutorial = db.relationship('Tutorial', backref=db.backref('participant', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


@dataclass
class Thread(db.Model):
	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	title = db.Column(db.Boolean, default=False, nullable=False)

	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	owner = db.relationship('User', backref=db.backref('threads', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


@dataclass
class CommentVote(db.Model):
	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	vote = db.Column(db.Boolean, default=False, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
	comment = db.relationship('Comment', backref=db.backref('votes', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


@dataclass
class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	text = db.Column(db.Boolean, default=False, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	owner = db.relationship('User', backref=db.backref('comments', lazy=True))

	parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
	parent_comment = db.relationship(
		'Comment', backref=db.backref('child_comments', lazy=True), remote_side="Comment.id")
	thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=True)
	thread = db.relationship('Thread', backref=db.backref('comments', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title


@dataclass
class File(db.Model):
	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	title = db.Column(db.Boolean, default=False, nullable=False)

	thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
	thread = db.relationship('Thread', backref=db.backref('files', lazy=True))

	def __repr__(self):
		return '<Post %r>' % self.title