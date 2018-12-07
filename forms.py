# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp

class SignupForm(FlaskForm):
    username = StringField('Public username', validators=[Regexp(r'^[\w.@+_-]+$', message="Username can only be composed of alphanumeric characters, and the symbols @+_-."), DataRequired("Please enter your username."), Length(max=255, message="Usernames cannot exceed 255 characters.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address."), Length(max=320, message="Email address is too long.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, max=255, message="Passwords must be between 6 and 255 characters.")])
    accept_tos = BooleanField('I have read and agree to the <a href="policy">terms of service and privacy policy</a>.', validators=[DataRequired("You can only use this service if you agree to the terms.")])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address."), Length(max=320, message="Email address is too long.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
    submit = SubmitField('Login')
