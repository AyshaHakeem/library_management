from flask import Blueprint, render_template, request, session, flash, jsonify
from library_flask import db
from library_flask.models import Member, Book, Transaction
from flask_login import login_required, current_user
from datetime import datetime
from library_flask.utils import get_user, get_members, get_books, get_transaction
import requests
today = datetime.now().date()

books = Blueprint('books', __name__)

@books.route('/books', methods=["GET", "POST"])
@login_required
def display_books():
    user = get_user()
    books = user.books_added
    return render_template('books.html', books=books)

@books.route('/import_books', methods=["GET", "POST"])
@login_required
def import_books():
    if request.args:
        args = request.args
        title, authors, publisher = args.get('title'), args.get('authors'), args.get('publisher')
        url = "https://frappe.io/api/method/frappe-library?"
        parameters = ''
        if title:
            parameters += f"title={title}&"
        if authors:
            parameters += f"authors={authors}&"
        if publisher:
            parameters += f"publisher={publisher}"

        try:
            response = requests.get(url + parameters)
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()
            if data.get('message'):
                session['books'] = data['message']
                return render_template('import-books.html', books=data['message'], title=title, authors=authors, publisher=publisher)
            else:
                return render_template('import-books.html', title=title, authors=authors, publisher=publisher, no_books='True')
        
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            flash('An error occurred while trying to import books', 'error')
            return render_template('import-books.html')

    if request.method == "POST":
        data = request.form
        books = session.get('books')
        selected_books = data.getlist('books')
        filtered_books = [book for book in books if book['bookID'] in selected_books]
        for book in filtered_books:
            filter_criteria = {'book_id': book['bookID'], 'user_id': current_user.id}
            existing = Book.query.filter_by(**filter_criteria).first() 
            if not existing:
                new_book = Book(
                    title= book['title'],
                    authors= book['authors'],
                    publisher = book['publisher'],
                    rating= book['average_rating'],
                    isbn= book['isbn'],
                    book_id = book['bookID'],
                    user_id=current_user.id
                )
                db.session.add(new_book)
        db.session.commit() 
        flash('Book(s) imported successfully', 'success')
    return render_template('import-books.html')

@books.route('/book-issue', methods=['GET', 'POST'])
@login_required
def issue_books():
    if request.method == 'GET':
        members_filter_criteria = [
            Member.user_id == current_user.id,
            Member .amount_outstanding < 500
        ]
        books_filter_criteria = {'user_id': current_user.id, 'booked': False}
        members = get_members(members_filter_criteria)
        books = get_books(books_filter_criteria)
        return render_template('book-issue.html', members=members, books=books)

    data = request.form
    book = Book.query.get(data['book'])
    member = Member.query.get(data['member'])

    
    # update book record
    if book and member: 
        if member.amount_outstanding<500 and book not in member.books:
            book.booked = True
            book.member_id = data['member']
            #  record transaction
            transaction = Transaction(
                member_email = member.email,
                description = f'Book issued to member - {today}',
                book = data['book'],
                book_title = book.title,
                member_id = data['member'],
                booked_date = data['issue'],  
                monthly_amount = data['monthly_amount'],
                user_id = current_user.id,
            )
            db.session.add(transaction)
            db.session.commit()
            flash('Book issued successfully!', 'success')
        else:
            flash('Could not issue book', 'error')
    return render_template('book-issue.html')

@books.route('/book-return', methods=['GET', 'POST'])
@login_required
def return_book():
    if request.method == 'GET':
        members_filter_criteria = [ Member.user_id == current_user.id ]
        members = get_members(members_filter_criteria)
        return render_template('book-return.html', members=members)
    data = request.form
    filter_criteria = {'user_id': current_user.id, 'member_id': data['member'], 'book': data['book'] }
    transaction = get_transaction(filter_criteria)
    book = Book.query.get(data['book'])
    member = Member.query.get(data['member'])
    try:
        if book:
            book.booked = False
            book.member_id = None
            member.amount_outstanding = data['outstanding_amount']
        if transaction:
            transaction.return_date = data['return']
            transaction.total_amount= data['total_amount'] or 0
            transaction.received_amount= data['received_amount'] or 0
            transaction.description = f'{transaction.description}\nBook returned by member - {today}'
        db.session.commit()
        flash('Book returned to library', 'success')
    except:
        flash('Error recording book return', 'error')

    return render_template('book-return.html', message='Book returned by members')

@books.route('/get-issue-details', methods=["GET", "POST"])
@login_required
def get_issue_details():
    args = request.args
    member_id = args.get('member_id')
    if args.get('book_id'):
        filter_criteria = {'member_id': member_id, 'book': args.get('book_id')}
        transaction = get_transaction(filter_criteria)
        return jsonify({'result': transaction.booked_date, 'amount': transaction.monthly_amount})

    member = Member.query.get(member_id)
    books = [{'id': book.id, 'title': book.title} for book in member.books]
    return jsonify({'books': books})