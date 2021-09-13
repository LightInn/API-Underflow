from endpoints import *

db.create_all()

if __name__ == "__main__":
	app.run(debug=True)
	users = User(id=2, first_name="Breval", last_name="Le Floch", email="breval2000@live.fr", password="123"), \
	        User(id=3, first_name="Mathis", last_name="Gautier", email="mathis@gmail.com", password="123"), \
	        User(id=4, first_name="Andy", last_name="Cinquin", email="andy.cinquin@gmail.com", password="123"), \
	        User(id=4, first_name="Test", last_name="Test", email="Test@test", password="123")
	db.session.add_all(users)
	db.session.commit()
