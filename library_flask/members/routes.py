from flask import Blueprint, redirect, render_template, request, url_for, flash
from library_flask import db
from library_flask.models import Member
from flask_login import login_required, current_user
from library_flask.utils import get_user, get_transactions, is_admin

members = Blueprint('members', __name__)

@members.route("/add_member", methods=["GET", "POST"])
@login_required
def add_member():
    if request.method == "GET":
        return render_template('add-member.html')
    data = request.form  
    filter_criteria = {'email': data['userEmail'], 'username': data['userName']}
    exisitng_member = Member.query.filter_by(**filter_criteria).first()
    if(exisitng_member):
        flash('A member with the same email or username already exists.')
        return redirect(url_for("members.add_member"))
    new_member = Member(
        fullname=data['userFullName'],
        username=data['userName'],
        email=data['userEmail'],
        user_id=current_user.id
    )
    db.session.add(new_member)
    db.session.commit()

    flash(f'New library member {data["userFullName"]} added', 'success')
    return render_template('add-member.html')

@members.route('/members/')
@login_required
def display_members():
    user = get_user()
    members = user.members_added
    return render_template('members.html', members=members)

@members.route('/members/<int:memberID>')
@login_required
def get_member(memberID):
    member = Member.query.get(memberID)
    if is_admin(member.user_id):
        # filter_criteria = {'user_id': current_user.id, 'member': memberID}
        # transactions = get_transactions(filter_criteria) or None
        transactions = member.member_transactions or None
        return render_template('member.html', member = member, transactions=transactions)
    else:
        return 'You are not authorized to access this page'

@members.route('/members/<int:memberID>/edit', methods=["GET", "POST"])
@login_required
def edit_member(memberID):
    member = Member.query.get(memberID)
    if is_admin(member.user_id):
        if request.method == "POST":
            data=request.form
            member.fullname = data['fullname']
            member.amount_outstanding = data['outstanding_amount']
            db.session.commit()
            flash('Member details updated','success')
            return redirect(f'/members/{member.id}')
        return render_template('edit-member.html', member = member)
    else:
        return 'You are not authorized to access this page'
