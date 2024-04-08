from library_flask import db 
from datetime import datetime

class User:
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    isAdmin = db.Column(db.Boolean, default=False)
    books = db.relationship('Book', backref='bookedBy', lazy=True)
    amount_outstanding = db.Column(db.Float)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    authors = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float)
    booked = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    user = db.relationship('User', back_populates='books')  
    
    def __repr__(self):
        return f"Book('{self.title}', 'booking status: {self.booked}'"


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booked_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    amount_paid = db.Column(db.Boolean)
    description = db.Column(db.String(255))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book', backref='transactions')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='transactions')

    def __repr__(self):
        return f"Transaction(id={self.id}, booked_date={self.booked_date}, return_date={self.return_date}, amount={self.amount}, amount_paid={self.amount_paid}, description={self.description})"
