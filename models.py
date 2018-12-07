# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask_sqlalchemy import SQLAlchemy

from passlib.hash import pbkdf2_sha256

from datetime import datetime

db = SQLAlchemy()

HASH_LEN = 87

class Quote(db.Model):
    __tablename__ = 'quote'
    qid = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255), nullable=False)
    work = db.Column(db.String(255), nullable=False)
    sentence = db.Column(db.String(1023), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(320), nullable=False, unique=True)
    account_type = db.Column(db.Integer, nullable=False)
    joined = db.Column(db.Integer, nullable=False)
    latest_login = db.Column(db.Integer, nullable=False)
    pwd_hash = db.Column(db.String(HASH_LEN))

    def __init__(self, username, email, account_type, password):
        self.username = username
        self.email = email
        self.account_type = account_type
        self.joined = int((datetime.today()).timestamp())
        self.latest_login = int((datetime.today()).timestamp())
        self.pwd_hash = self.generate_password_hash(password)

    def generate_password_hash(self, pwd):
        return pbkdf2_sha256.hash(pwd)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.pwd_hash)

class Quiz(db.Model):
    __tablename__ = 'quiz'
    quiz_id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    is_solved = db.Column(db.Boolean, nullable=False)
    quotes = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)
