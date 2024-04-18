from library_flask import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# class Library(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True)
#     tagline = db.Column(db.String(200), index=True, unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    isAdmin = db.Column(db.Boolean, default=True)
    books_added = db.relationship('Book', backref='user', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    members_added = db.relationship('Member', backref='user', lazy=True)
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, index=True)
    title = db.Column(db.String(300), nullable=False)
    authors = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Float)
    publisher = db.Column(db.String(300))
    isbn = db.Column(db.String(120))
    booked = db.Column(db.Boolean, default=False, nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id')) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'{self.id}'
    
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    books = db.relationship('Book', backref='member', lazy=True)
    amount_outstanding = db.Column(db.Float, default=0.0)
    member_transactions = db.relationship('Transaction', backref='member', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.id}'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    booked_date = db.Column(db.DateTime, default=datetime.date)
    return_date = db.Column(db.DateTime)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    # member = db.Column(db.Integer)
    member_email = db.Column(db.String(150))
    book = db.Column(db.Integer, db.ForeignKey('book.id'))
    book_title = db.Column(db.String(150))
    monthly_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float)
    # received_amount = db.Column(db.Boolean)
    received_amount = db.Column(db.Float)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.id}'
