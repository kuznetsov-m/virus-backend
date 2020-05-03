from flask import Flask, jsonify, request, render_template, redirect, url_for, request, session, flash, g, \
    make_response, abort, send_file
from sys import argv
from functools import wraps
import sqlite3

import os
import json

from db_connector import DbConnector

app = Flask(__name__)
# app.config.from_object('config')
app.secret_key = 'my secret key'
app.database = 'sample.db'

db_connector = DbConnector(app.database)
db_connector.create_event('05.05.2020', '15:00', 'first test event', 1)

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
    # g.db = connect_db()
    # cur = g.db.execute('select * from posts')
    # posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    # g.db.close()
    posts = []
    return render_template('index.html', posts=posts)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/timetable')
@login_required
def timetable():
    events = db_connector.get_all_events()
    return render_template('timetable.html', events=events)


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


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404


# ------------------------------------------------------------
@app.route('/users/<int:id>.png')
def get_image(id):
    file_path = f'users/{id}.png'
    if not os.path.isfile(file_path):
        abort(404)
    return send_file(file_path, mimetype='image/png')

@app.route('/api/timetable')
def api_timetable():
    events = db_connector.get_all_events()
    return jsonify(events), 201

@app.route('/api/create_event', methods=['POST'])
def create_event():
    if not request.json or not 'date' in request.json \
                        or not 'time' in request.json \
                        or not 'description' in request.json \
                        or not 'user_id' in request.json:
        abort(400)
    event = {
        'date': request.json['date'],
        'time': request.json['time'],
        'description': request.json.get('description', ""),
        'user_id': request.json['user_id'],
    }
    db_connector.create_event_from_dict(event)

    return jsonify(event), 201

#-------------------------------------------------------------
def connect_db():
    return sqlite3.connect(app.database)


if __name__ == "__main__":
    if len(argv) == 2:
        app.run(host='0.0.0.0', port=int(argv[1]))
    else:
        app.run(port=8080, debug=True) 