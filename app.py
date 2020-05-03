from flask import Flask, jsonify, request, render_template, redirect, url_for, request, session, flash, g
from sys import argv
from functools import wraps
import sqlite3

import json

app = Flask(__name__)
# app.config.from_object('config')
app.secret_key = 'my secret key'
app.database = 'sample.db'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def home():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('index.html', posts=posts)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/timetable')
@login_required
def timetable():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('timetable.html', posts=posts)


@app.route('/conversation_request', methods=['GET', 'POST'])
@login_required
def conversation_request():
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        flash(f'date: {date} description: {description}')
    return render_template('conversation_request.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' \
                or request.form['password'] != 'admin':
            error = 'Invalid creditials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('home'))


# ------------------------------------------------------------
@app.route('/api/timetable')
def api_timetable():
    event = {'date': '05.05.2020', 'description': 'event description'}
    date = [event, event]
    return json.dumps(date)

#-------------------------------------------------------------
def connect_db():
    return sqlite3.connect(app.database)


if __name__ == "__main__":
    if len(argv) == 2:
        app.run(host='0.0.0.0', port=int(argv[1]))
    else:
        app.run(port=8080, debug=True) 