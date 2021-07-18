from flask import Flask
from flask import request, make_response, abort
from database import *
import json
from dateutil import parser

app = Flask(__name__)

@app.route('/')
def welcome():
    return "<p>Welcome to Kai and Mel's RSVP. Use your URL to RSVP.</p>"

@app.route('/rsvp/<int:guest_id>')
def get_rsvp(guest_id):
    guest = Guest.query.get(guest_id)
    if guest is None:
        abort(404)
    plus_one = Guest.query.get(guest.plus_one) if guest.plus_one else None
    response = {}
    response['name'] = guest.name
    response['plus_one'] = plus_one.name
    response['email'] = guest.email
    return json.dumps(response)

@app.route('/rsvp/<int:guest_id>', methods=['POST'])
def post_rsvp(guest_id):
    guest = Guest.query.get(guest_id)
    if guest is None:
        abort(404)

    f = request.form

    rsvp = RSVP (
        guest_id = guest_id,
        wedding = f['wedding'] == 'TRUE',
        cocktails = f['cocktails'] == 'TRUE',
        hike = f['hike'] == 'TRUE'
    )
    brunch = f.get('brunch')
    rsvp.brunch = brunch == 'TRUE' if brunch else None

    rsvp.phone = f.get('phone')
    rsvp.cocktails_excess = f.get('cocktails_excess')

    vaxxed = f.get('vaxxed')
    masked = f.get('masked')
    rsvp.vaxxed = vaxxed == 'TRUE' if vaxxed else None
    rsvp.masked = masked == 'TRUE' if masked else None

    Session.add(rsvp)
    Session.commit()

    return ''

# TODO: Marshallow
