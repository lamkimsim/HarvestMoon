import datetime
import logging

from flask import Flask, render_template, request, Response, jsonify
import sqlalchemy



app = Flask(__name__)

logger = logging.getLogger()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)