from endpoints import *

db.create_all()

if __name__ == "__main__":
	app.run(load_dotenv=True, port=os.getenv('PORT'), debug=(os.getenv('DEBUG') == '1'))
