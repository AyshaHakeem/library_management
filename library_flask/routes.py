from library_flask import app
from flask import request, jsonify
from library_flask.models import User, Book, Transaction


@app.route('/api/data')
def get_data():
    data = [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'}
    ]
    return jsonify(data)

@app.route('/')
def home():
    return '<h1>Hiyyaaa</h1>'

@app.route('/members/', defaults={'memberID': None})
@app.route('/members/<int:memberID>')
def get_member(memberID):
    if memberID is None:
        # get User record 
        return "All members"
    else:
        # get User record 
        # get Transaction(s) if any
        return f"Member with ID: {memberID}"
    
@app.route('/book_issue', methods=['GET', 'POST'])
def issue_book():
    # get book record
    # if !book.booked 
    # get user record
    # if user.amount_outstanding < 500 
    # record transaction
    # link the book
 
    return "Book Issued"

@app.route('/book_return', methods=['GET', 'POST'])
def return_book():
    # get user record
    # get book record
    # if user.books includes book
    # record transaction 
    # unlink book, set outstanding amount

    return "Book returned"


@app.route('/transactions')
def list_transactions():
    # List all transactions
    return 'View transactions'

@app.route('/transactions/<int:transactionID>')
def view_transaction(transactionID):
    # View transaction details
    return f"Transaction with ID: {transactionID}"

@app.route("/transactions/<int:transactionID>", methods=['DELETE'])
def delete_transaction(transactionID):
    # Delete transaction
    return 'Delete transaction'

@app.route('/transactions/<int:transactionID>/edit', methods=['GET', 'POST'])
def update_transaction(transactionID):
    if request.method == 'GET':
        # Display form to edit transaction
        return 'Display edit form'
    elif request.method == 'POST':
        # Update transaction
        return 'Transaction updated'
