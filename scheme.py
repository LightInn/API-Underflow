import uuid
from datetime import datetime
from dataclasses import dataclass
import bcrypt
import pytz
from sqlalchemy import DECIMAL

from conf import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import UUIDType


@dataclass
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)


@dataclass
class User(db.Model):
    id: str
    first_name: str
    last_name: str
    email: str
    activated: bool
    admin: bool
    created_on: datetime
    last_login: datetime
    classe: Class

    id = db.Column(UUIDType(binary=False), primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=False, nullable=False)
    activated = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    admin = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=False)
    last_login = db.Column(db.DateTime, unique=False, nullable=True)

    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=True)
    classe = db.relationship('Class', backref=db.backref('users', lazy='dynamic'))

    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

    def verify_password(self, password):
        return bcrypt.checkpw(password, self.password_hash)


@dataclass
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)


@dataclass
class Proposition(db.Model):
    id: int
    title: str
    date_butoir: datetime
    classe: Class
    subject: Subject

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    date_butoir = db.Column(db.DateTime, nullable=False)

    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    classe = db.relationship('Class', backref=db.backref('propositions', lazy='dynamic'))

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', backref=db.backref('propositions', lazy='dynamic'))


@dataclass
class Course(db.Model):
    id: int
    title: str
    description: str
    date_start: datetime
    duration: DECIMAL(2, 1)
    ended: bool
    classe: Class
    subject: Subject
    owner: User

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_start = db.Column(db.DateTime, nullable=False)
    duration = db.Column(DECIMAL(2, 1), nullable=True)
    ended = db.Column(db.Boolean, nullable=False)

    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    classe = db.relationship('Class', backref=db.backref('courses', lazy='dynamic'))

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', backref=db.backref('courses', lazy='dynamic'))

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('courses_owner', lazy='dynamic'))


@dataclass
class CourseSubscription(db.Model):
    id: int
    confirmed: bool
    participant: User
    course: Course

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)

    participant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    participant = db.relationship('User', backref=db.backref('course_participation', lazy='dynamic'))

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref=db.backref('participant', lazy='dynamic'))


@dataclass
class Thread(db.Model):
    id: int
    title: str
    owner: User

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Boolean, default=False, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('threads', lazy='dynamic'))


@dataclass
class Comment(db.Model):
    id: int
    text: str
    created_on: datetime
    owner: User
    thread: Thread

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Boolean, default=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Europe/Paris')))

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))

    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    parent_comment = db.relationship(
        'Comment', backref=db.backref('child_comments', lazy='dynamic'), remote_side="Comment.id")
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=True)
    thread = db.relationship('Thread', backref=db.backref('comments', lazy='dynamic'))


@dataclass
class CommentVote(db.Model):
    id: int
    vote: int
    created_on: datetime
    comment: Comment

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vote = db.Column(db.Boolean, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Europe/Paris')))

    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    comment = db.relationship('Comment', backref=db.backref('votes', lazy='dynamic'))


@dataclass
class File(db.Model):
    id: int
    title: str
    link: str
    thread: Thread

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), default=False, nullable=False)
    link = db.Column(db.Boolean, unique=False, nullable=False)

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    thread = db.relationship('Thread', backref=db.backref('files', lazy='dynamic'))
