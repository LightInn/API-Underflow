from endpoints import *

db.create_all()
# new_user = User(first_name='Mathis', last_name='Gauthier', email='mathis.gauthier@epsi.fr',
#                 password=bcrypt.hashpw(b'123456', salt=bcrypt.gensalt()))
# db.session.add(new_user)
# db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
