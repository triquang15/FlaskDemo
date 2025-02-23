from flask import Flask
from app.extension import db, migrate

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate.init_app(app, db)

from app.models.user import User
from app.models.companies import Company
from app.models.books import Book

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
