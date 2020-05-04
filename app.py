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
app.config['USERS'] = os.path.join('users')

db_connector = DbConnector(app.database)
db_connector.create_user('m-wazowski@gmail.com', '1234', \
                        'Mike', 'Wazowski', 2, 'User description text')
db_connector.create_user('g-house@gmail.com', '1234', \
                        'Gregory', 'House', 1, 'Unconventional, misanthropic medical genius')
db_connector.create_event("05.05.2020", '15:00', 'event description', 1)
db_connector.create_event("05.05.2020", '12:00', 'my description', 1)
db_connector.create_event("06.05.2020", '12:00', 'event description', 1)
db_connector.create_event("10.05.2020", '13:00', 'consilium', 2)

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


@app.route('/users')
@login_required
def users():
    users = db_connector.get_all_users()
    return render_template('users.html', users=users)


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
@app.route('/api/create_user', methods=['POST'])
def api_create_user():
    if not request.json or not 'login' in request.json \
                        or not 'password' in request.json \
                        or not 'first_name' in request.json \
                        or not 'last_name' in request.json \
                        or not 'role_id' in request.json \
                        or not 'description' in request.json:
        abort(400)
    user = {
        'login': request.json['login'],
        'password': request.json['password'],
        'first_name': request.json['first_name'],
        'last_name': request.json['last_name'],
        'role_id': request.json['role_id'],
        'description': request.json.get('description', ""),
    }

    if db_connector.check_exist_user(user['login']):
        return jsonify(error = 3), 201

    db_connector.create_user_from_dict(user)
    user_id = db_connector.get_user_id_by_login(user['login'])
    user['user_id'] = user_id

    return jsonify(user), 201


@app.route('/api/users')
def api_users():
    users = db_connector.get_all_users()
    return jsonify(users), 201


@app.route('/api/user_image/<int:id>.png')
def api_get_image(id):
    file_path = f'users/{id}.png'
    if not os.path.isfile(file_path):
        abort(404)
    return send_file(file_path, mimetype='image/png')


@app.route('/api/authentication', methods=['POST'])
def api_authentication():
    if not request.json or not 'login' in request.json \
                        or not 'password' in request.json:
        abort(400)
    login = request.json['login']
    password = request.json['password']
    
    if not db_connector.check_exist_user(login):
        return jsonify(error = 1), 201
    if not db_connector.check_valid_login_password(login, password):
        return jsonify(error = 2), 201

    user_id = db_connector.get_user_id_by_login(login)
    return jsonify(login=login, password=password, user_id=user_id), 201


@app.route('/api/timetable')
def api_timetable():
    events = db_connector.get_all_events()
    return jsonify(events), 201


@app.route('/api/user_events', methods=['POST'])
def api_user_events():
    if not request.json or not 'login' in request.json:
        abort(400)
    login = request.json['login']
    
    if not db_connector.check_exist_user(login):
        return jsonify(error = 1), 201
    
    events = db_connector.get_user_events(login)
    return jsonify(events), 201


@app.route('/api/create_event', methods=['POST'])
def api_create_event():
    if not request.json or not 'date' in request.json \
                        or not 'time' in request.json \
                        or not 'description' in request.json \
                        or not 'user_login' in request.json:
        abort(400)
    event = {
        'date': request.json['date'],
        'time': request.json['time'],
        'description': request.json.get('description', ""),
        'user_login': request.json['user_login'],
    }
    db_connector.create_event_from_dict(event)

    return jsonify(event), 201

# @app.route('/api/set_doctor_for_event', methods=['POST'])

#-------------------------------------------------------------
def connect_db():
    return sqlite3.connect(app.database)


if __name__ == "__main__":
    if len(argv) == 2:
        app.run(host='0.0.0.0', port=int(argv[1]))
    else:
        app.run(port=8080, debug=True) 