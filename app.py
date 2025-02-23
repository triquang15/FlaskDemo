from flask import Flask
from extension import db

app = Flask(__name__)
db.init_app(app)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
