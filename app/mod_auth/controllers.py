from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from views import authors, publishers
from models import Entry
from run import app



@login_required
def index():
    all_entries = Entry.query.order_by(Entry.id).filter_by(user_id=current_user.id).all()
    return render_template('index.html', books=all_entries)