from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import Entry
from app import db, app
from instance.config import app


# @login_required
@app.route('/', methods=['GET'])
def index():
    return render_template('budget/index.html')



@login_required
@app.route('/entries', methods=['GET'])
def list_entries():
    all_entries = Entry.query.order_by(Entry.id).filter_by(user_id=current_user.id).all()
    return render_template('budget/list_entries.html', books=all_entries)




@login_required
@app.route('/add_cost', methods=['GET', 'POST'])
def add_cost():
    if request.method =='POST':
        new_entry = Entry(request.form['name'],
                    request.form['amount'],
                    request.form['category_id'],
                    current_user.id)
        db.session.add(new_entry)
        db.session.commit()






@login_required
@app.route('/list_cost', methods=['GET'])
def list_cost():
    pass



@login_required
@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    if request.method =='POST':
        new_entry = Entry(
                    request.form['name'],
                    request.form['amount'],
                    request.form['category_id'],
                    current_user.id)
        db.session.add(new_entry)
        db.session.commit()





@login_required
@app.route('/list_income', methods=['GET'])
def list_income():
    pass


@login_required
@app.route('/report', methods=['GET', 'POST'])
def report():
    pass







