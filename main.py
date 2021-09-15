from endpoints import *

db.create_all()
users = User( first_name="Andy", last_name="Cinquin", email="andy.cinquin@gmail.com", password="123")
db.session.add(users)
db.session.commit()

if __name__ == "__main__":

	app.run(debug=True)
