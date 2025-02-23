from app.extension import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    password = db.Column(db.Text, nullable=False)
    biography = db.Column(db.Text, nullable=True)
    user_type = db.Column(db.String(20), default='author')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    
    def __init__(self, first_name, last_name, email, contact, password, biography, user_type, image=None):
        super(User, self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.password = password
        self.biography = biography
        self.user_type = user_type
        
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
        
    