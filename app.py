from flask import Flask, jsonify, request, render_template, redirect, url_for, request, session, flash, g
from sys import argv
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.secret_key = 'my secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

db = SQLAlchemy(app)

from models import *


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login2'))
    return wrap


@app.route('/')
@login_required
def home():
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', posts=posts)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/login2', methods=['GET', 'POST'])
def login2():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' \
                or request.form['password'] != 'admin':
            error = 'Invalid creditials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login2.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('home'))


def connect_db():
    return sqlite3.connect('posts.db')


if __name__ == "__main__":
    if len(argv) == 2:
        app.run(host='0.0.0.0', port=int(argv[1]))
    else:
        app.run(port=8080, debug=True) 