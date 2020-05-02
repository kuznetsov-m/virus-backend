from flask import Flask, jsonify, request, render_template
from sys import argv

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Test page</h1>"

@app.route('/login')
def login():
    return render_template('index.html')

if __name__ == "__main__":

    if len(argv) == 2:
        app.run(host='0.0.0.0', port=int(argv[1]))
    else:
        app.run(port=8080) 