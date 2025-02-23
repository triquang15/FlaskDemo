from flask import Flask
from app.extension import db, migrate, jwt
from app.controllers.auth.auth_controller import auth
from app.controllers.users.user_controller import users

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

from app.models.user import User
from app.models.companies import Company
from app.models.books import Book

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(users)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
