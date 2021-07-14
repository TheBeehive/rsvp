from flask import Flask
from flask import request
from db import *

app = Flask(__name__)

@app.route('/')
def welcome():
    return "<p>Welcome to Kai and Mel's RSVP. Use your URL to RSVP.</p>"

@app.route('/rsvp/<int:event_id>/<int:guest_id>', methods=['GET', 'POST'])
def rsvp(guest_id, event_id):
    if request.method == 'POST':
        do_rsvp(guest_id, event_id, request.form['value'])
        return 'Success'
