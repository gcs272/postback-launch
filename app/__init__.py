#!/usr/bin/env python
from flask import Flask, g, render_template, request
from storm.locals import *
import os

main = Flask(__name__)

class Email(object):
    __storm_table__ = 'emails'
    id = Int(primary=True)
    email = Unicode()

@main.before_request
def before_request():
    db = create_database('sqlite:data/postback.sqlite')
    g.store = Store(db)

@main.after_request
def after_request(response):
    g.store.close()
    return response

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'email' in request.form:
        email = Email()
        email.email = request.form.get('email', 'nobody')
        try:
            g.store.add(email)
            g.store.commit()
            return render_template('index.html', contacted=True)
        except:
            g.store.rollback()
            return render_template('index.html', duplicate=True)

    else:
        return render_template('index.html', contacted=False)
