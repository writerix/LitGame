# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
@author: James Bigland
"""

from flask import Flask, render_template, url_for, session, redirect, request

from sqlalchemy.exc import IntegrityError
from  sqlalchemy.sql.expression import func

from models import db, User, Quote, Quiz
from forms import SignupForm, LoginForm

import uuid
from datetime import datetime

from random import shuffle

from werkzeug import escape

import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SUPER SECRET DEV KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quote_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #this feature is not needed and adds overhead
db.init_app(app)
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict' #prevents sending cookies with all external requests

NUMQ = 3

ACCOUNT_TYPE_GUEST = 0
ACCOUNT_TYPE_REGULAR = 1
ACCOUNT_TYPE_CONVERTED = 2

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():

    conversion = False

    if 'email' in session:
        #user is regular, converted, or guest type
        user = User.query.filter_by(email=session['email']).first()
        if user.account_type != ACCOUNT_TYPE_GUEST:
            return redirect(url_for('game'))
        else:
            conversion = True

    signup = SignupForm()

    if request.method == "GET":
        return render_template('signup.html', form=signup, feedback = '')
    else:
        if signup.validate() == False:
            return render_template('signup.html', form=signup, feedback = '')
        else:
            try:
                if conversion == False:
                    newuser = User(signup.username.data, signup.email.data, ACCOUNT_TYPE_REGULAR, signup.password.data)
                    db.session.add(newuser)
                    db.session.commit()
                    session['email'] = newuser.email
                else:
                    #update database
                    user.username = signup.username.data
                    user.email = signup.email.data
                    user.account_type = ACCOUNT_TYPE_CONVERTED
                    user.pwd_hash = user.generate_password_hash(signup.password.data)
                    db.session.commit()
                    #remove old guest from session
                    session.pop('email', None)
                    #add new converted user to session
                    session['email'] = user.email
                return redirect(url_for('game'))
            except IntegrityError:
                db.session.rollback()
                #username or email is not unique
                error_msg = ""
                if (User.query.filter_by(username = newuser.username).first()) is not None:
                    error_msg += "Username " + newuser.username + " is already taken. "
                if (User.query.filter_by(email = newuser.email).first()) is not None:
                    error_msg += "Only one account per email address is permitted."
                return render_template('signup.html', form=signup, feedback = error_msg)
            except Exception as e:#except:
                #other error
                db.session.rollback()
                error_msg = "Unknown error." + str(e)
                return render_template('signup.html', form=signup, feedback = error_msg)


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'email' in session:
        return redirect(url_for('game'))

    login = LoginForm()
    if request.method == "GET":
        return render_template('login.html', form=login, feedback='')
    else:
        if login.validate() == False:
            return render_template('login.html', form=login, feedback='')
        else:
            user = User.query.filter_by(email=login.email.data).first()
            if user is not None and user.check_password(login.password.data):
                session['email'] = login.email.data
                user.latest_login = int((datetime.today()).timestamp())
                db.session.commit()
                return redirect(url_for('game'))
            else:
                return render_template('login.html', form=login, feedback='Email address not found or password incorrect.')

@app.route('/guest_account')
def guest_account():
    if 'email' in session:
        return redirect(url_for('game'))

    guest_name = "guest #" + str(uuid.uuid4())
    guest_email = guest_name + "@example.com"

    while User.query.filter_by(username = guest_name).first() is not None and User.query.filter_by(email = guest_email).first is not None:
        guest_name = "guest #" + str(uuid.uuid4())
        guest_email = guest_name + "@example.com"

    try:
        user = User(guest_name, guest_email, ACCOUNT_TYPE_GUEST, str(uuid.uuid4()))
        db.session.add(user)
        db.session.commit()
        session['email'] = user.email
    except:
        #fail silently
        db.session.rollback()
        return redirect(url_for('game'))
    return redirect(url_for('game'))

@app.route('/populate_quotes/<author>', methods=['POST'])
def populate_quotes(author):
    #users must be signed in or have guest account
    if 'email' not in session:
        return redirect(url_for('guest_account'))
    #begin game
    user = User.query.filter_by(email = session['email']).first()
    quotes = []
    sources = Quote.query.filter_by(author = author).with_entities(Quote.work).distinct().order_by(Quote.work).all()
    sources = [item[0] for item in sources]
    shuffle(sources)
    sources = sources[:NUMQ]

    for a_source in sources:
        quotes.append(Quote.query.filter_by(author = author).filter_by(work = a_source).order_by(func.random()).first())

    for selection in quotes:
        selection.work = escape(selection.work)
        selection.sentence = (selection.sentence).replace('"', '&quot;')

    db_json = '''{"works": ["''' + quotes[0].work + '''", "''' + quotes[1].work + '''", "''' + quotes[2].work + '''"], "sentences": ["''' + quotes[0].sentence +'''", "''' + quotes[1].sentence + '''", "''' + quotes[2].sentence + '''"]}'''
    db_json = db_json.replace('\\&quot;', '&quot;')
    db_json = db_json.replace('\&quot;','&quot;')
    db_json = db_json.replace("\\'", "'")
    db_json = db_json.replace('\n', '')
    db_json = db_json.replace('\r', '')
    quiz = Quiz(uid = user.uid, is_solved = False, quotes = db_json, score = 0)
    db.session.add(quiz)
    db.session.commit()

    if user.account_type == 0:
        username = 'Signed in as: Guest.'
    else:
        username = "Signed in as: " + escape(user.username)

    out_json = '''{"account_type": ''' + str(user.account_type) + ''', "username": "''' + username +'''", "quiz_id": "''' + str(quiz.quiz_id) + '''", "works": ["''' + quotes[0].work + '''", "''' + quotes[1].work + '''", "''' + quotes[2].work + '''"], "sentences": ["'''
    shuffle(quotes)

    out_json += quotes[0].sentence +'''", "''' + quotes[1].sentence + '''", "''' + quotes[2].sentence + '''"]}'''
    out_json = out_json.replace('\\&quot;', '&quot;')
    out_json = out_json.replace('\&quot;', '&quot;')
    out_json = out_json.replace("\\'", "'")
    out_json = out_json.replace('\n', '')
    out_json = out_json.replace('\r', '')

    return out_json


@app.route('/grade_quiz/<quiz_id>', methods=['POST'])
def grade_quiz(quiz_id):
    user = User.query.filter_by(email = session['email']).first()
    quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
    if quiz is None:
        return "Error: quiz not found."
    if quiz.is_solved != 0:
        return "Error: this quiz has already been solved once before."
    if quiz.uid != user.uid:
        return "An authentication error has occurred. Please try logging out then back in again."
    instr = (request.data).decode('utf-8')

    score = 0
    marked = [False, False, False]
    if quiz.quotes == instr:#perfect match
        score = 3
        marked = [True, True, True]
    else:
        in_data = json.loads(instr)
        db_data = json.loads(quiz.quotes)
        for i in range(NUMQ):
            if in_data["sentences"][i] == db_data["sentences"][i]:
                score += 1
                marked[i] = True
    quiz.score = score
    quiz.is_solved = True
    db.session.commit()

    total_score = db.session.query(func.sum(Quiz.score)).filter_by(uid = user.uid).scalar()
    total_attemps = db.session.query(func.count(Quiz.quiz_id)).filter_by(uid = user.uid).scalar()
    percent = round((total_score / (total_attemps * NUMQ)) * 100, 2)
    percent = str(percent) + "%"

    ret_dict = {"score" : score, "total_score": total_score, "percent": percent, "answers": marked}

    return json.dumps(ret_dict)

@app.route('/game')
def game():
    #users must be signed in or have guest account
    if 'email' not in session:
        return redirect(url_for('guest_account'))

    #begin game by allowing user to choose from available authors
    tup_authors = Quote.query.with_entities(Quote.author).distinct().order_by(Quote.author).all()
    all_authors = [item[0] for item in tup_authors]

    return render_template('game.html', option_list = all_authors)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/delete_account', methods=["GET","DELETE"])
def delete_account():
    if request.method == "GET":
        return redirect(url_for('index'))

    #users must be logged in to delete their accounts
    if 'email' not in session:
        return str("/")

    user = User.query.filter_by(email=session['email']).first()
    if user is None:
        return str("/")
    #delete user quiz details and user account
    db.session.query(Quiz).filter_by(uid = user.uid).delete()
    db.session.delete(user)
    db.session.commit()
    #logout user
    session.pop('email', None)
    #redirect happens in browser js
    return str("/")

@app.route('/policy')
def policy():
    return render_template('policy.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)#optional args
