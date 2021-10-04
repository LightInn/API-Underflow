from flask import jsonify

from conf import app
from scheme import *


# Endpoint to test the API connectivity
@app.route("/api/test/")
def test():
	return jsonify({
		'status': 'ok'
	})


# Endpoint to get a list of all users
@app.route("/api/users/", methods=['GET'])
def users():
	users = User.query.all()
	return jsonify(users)


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
