from flask import Blueprint, redirect, render_template, request
from library_flask.models import Member, Transaction
from flask_login import login_required
from library_flask.utils import get_user, is_admin

transactions = Blueprint('transactions', __name__)

@transactions.route('/transactions')
@login_required
def display_transactions():
    user = get_user()
    transactions = user.transactions
    return render_template('transactions.html', transactions=transactions)

@transactions.route('/transactions/<int:transactionID>')
@login_required
def view_transaction(transactionID):     
    transaction = Transaction.query.get(transactionID)
    if is_admin(transaction.user_id):
        member = Member.query.get(transaction.member_id)
        return render_template('transaction.html', transaction = transaction, member=member)
    else:
        return 'You are not authorized to access this page'