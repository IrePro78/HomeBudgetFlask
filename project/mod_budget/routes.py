from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from sqlalchemy import func

from . import budget_blueprint
from models import Entry, Category
from project import db


@budget_blueprint.route('/', methods=['GET'])
def index():
    return render_template('budget/index.html')


@budget_blueprint.route('/list_entries', methods=['GET', 'POST'])
@login_required
def list_entries():
    all_entries = Entry.query.order_by(Entry.id).filter_by(user_id=current_user.id).all()
    saldo = db.session.query(func.sum(Entry.amount)).filter_by(user_id=current_user.id).scalar()
    return render_template('budget/list_entries.html', entries=all_entries, saldo='Brak' if saldo is None else saldo)



@budget_blueprint.route('/add_cost', methods=['GET', 'POST'])
@login_required
def add_cost():
    if request.method == 'POST':
        category_id = add_category()
        amount = float(request.form['amount']) * -1
        new_entry = Entry(request.form['title'],
                          amount,
                          category_id,
                          current_user.id)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('budget.list_entries'))
    return render_template('budget/add_cost.html')



@budget_blueprint.route('/list_cost', methods=['GET'])
@login_required
def list_cost():
    pass




@budget_blueprint.route('/add_income', methods=['GET', 'POST'])
@login_required
def add_income():
    if request.method == 'POST':
        category_id = add_category()
        new_entry = Entry(
            request.form['title'],
            float(request.form['amount']),
            category_id,
            current_user.id)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('budget.list_entries'))
    return render_template('budget/add_income.html')


@budget_blueprint.route('/list_income', methods=['GET'])
@login_required
def list_income():
    pass


@budget_blueprint.route('/add_cost', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        new_category = Category(request.form['category'])
        db.session.add(new_category)
        db.session.commit()
        return new_category.id



@budget_blueprint.route('/edit_entry', methods=['GET', 'POST'])
@login_required
def edit_entry():
    if request.method == 'POST':
        entry = Entry.query.get(request.form.get('id'))
        entry.id = request.form['id']
        entry.title = request.form['title']
        entry.amount = request.form['amount']
        entry.category_id = request.form['category_id']
        db.session.commit()
        flash('Wpis został zaktualizowany!', 'info')
        return redirect(url_for('budget.list_entries'))
    return render_template('budget/edit_entry.html')










@budget_blueprint.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    pass
