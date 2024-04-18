from library_flask.models import User, Member, Book, Transaction
from flask_login import current_user

def is_admin(id):
    admin = User.query.get(current_user.id)
    return admin.id == id

def get_user():
    return User.query.get(current_user.id)

def get_members(filter_criteria):
    return Member.query.filter(*filter_criteria).all()

def get_books(filter_criteria):
    return Book.query.filter_by(**filter_criteria).all()

def get_transactions(filter_criteria):
    return Transaction.query.filter_by(**filter_criteria).all()

def get_transaction(filter_criteria):
    return Transaction.query.filter_by(**filter_criteria).first()