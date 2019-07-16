from flask import render_template, url_for, flash, redirect, request

from dream_journal import app, db
from dream_journal.forms import DreamForm
from dream_journal.models import Dreams
from dream_journal.symbol import symbol_dictionary
from datetime import date
import datetime

def get_symbols(dream_title):
    symbols = {}
    words = dream_title.split(" ")
    for word in words:
        key_word = word.capitalize()
        if key_word in symbol_dictionary:
            symbols[key_word] = symbol_dictionary.get(key_word)
    return symbols


# def set_dream_symbols(dreams):
#     for dream in dreams:
#         dream['symbols'] = get_symbols(dream.title)
#     return dreams


def get_dream_record_history(dreams):
    list_of_dates = [dream.dream_date for dream in dreams]
    dream_record_days = len(set(list_of_dates))
    start_date = min(list_of_dates)
    today = datetime.datetime.now()
    total_days = (start_date - today).days
    return start_date,dream_record_days,total_days


@app.route("/")
@app.route("/home")
def home():
    dreams = Dreams.query.order_by(Dreams.dream_date.desc()).all()
    # dreams = set_dream_symbols(dreams)
    start_date,dream_recorded,dream_not_recorded = get_dream_record_history(dreams)
    return render_template('home.html', dreams=dreams, start_date=start_date, get_symbols=get_symbols,
                           dream_recorded=dream_recorded, dream_not_recorded=dream_not_recorded)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/dream/new", methods=['GET', 'POST'])
def log_dream():
    form = DreamForm()
    if form.validate_on_submit():
        dream = Dreams(title=form.title.data, dream_date=form.dream_date.data)
        db.session.add(dream)
        db.session.commit()
        flash('Your dream has been logged!', 'success')
        return redirect(url_for('home'))
    return render_template('log_dream.html', title='New Dream', form=form, legend='Log New Dream')


@app.route("/dream/<int:dream_id>")
def view_dream(dream_id):
    dream = Dreams.query.get_or_404(dream_id)
    symbols = get_symbols(dream.title)
    return render_template('dream.html', title=dream.title, dream=dream, symbols=symbols)
