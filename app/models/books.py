from app.extension import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    price_unit = db.Column(db.String(10), nullable=False, default='USD')
    published_at = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(20), nullable=False, unique=True)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    user = db.relationship('User', backref=db.backref('books'))
    company = db.relationship('Company', backref=db.backref('books'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    
    def __init__(self, title, pages, price, published_at, isbn, genre, user_id, company_id, price_unit, description, image=None):
        super(Book, self).__init__()
        self.title = title
        self.pages = pages
        self.price = price
        self.published_at = published_at
        self.isbn = isbn
        self.genre = genre
        self.user_id = user_id
        self.company_id = company_id
        self.price_unit = price_unit
        self.description = description
        self.image = image
        
    def __repr__(self):
        return f"Book: {self.title}"
        