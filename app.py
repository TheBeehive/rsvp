from flask import Flask
from flask import request, make_response, abort
from db import *
import json
from dateutil import parser

app = Flask(__name__)

@app.route('/')
def welcome():
    return "<p>Welcome to Kai and Mel's RSVP. Use your URL to RSVP.</p>"

@app.route('/rsvp/<int:guest_id>')
def get_rsvp(guest_id):
    guest = RSVP.query.get(guest_id)
    if guest is None:
        abort(404)
    plus_one = RSVP.query.get(guest.plus_one) if guest.plus_one else None
    response = {}
    response['guest_name'] = guest.guest_name
    response['plus_one'] = plus_one.guest_name
    response['email'] = guest.email
    return json.dumps(response)

@app.route('/rsvp/<int:guest_id>', methods=['PUT'])
def put_rsvp(guest_id):
    guest = RSVP.query.get(guest_id)
    if guest is None:
        abort(404)

    j = request.json
    time = j.get('time')
    if time is None:
        # Timestamp required
        abort(400)

    guest.update_with_put('brunch', j.get('brunch'), parser.parse(time))
    guest.update_with_put('wedding', j.get('wedding'), parser.parse(time))
    guest.update_with_put('vaxxed', j.get('vaxxed'), parser.parse(time))
    guest.update_with_put('masked', j.get('masked'), parser.parse(time))
    guest.update_with_put('hike', j.get('hike'), parser.parse(time))
    guest.update_with_put('phone', j.get('phone'), parser.parse(time))
    guest.update_with_put('cocktails', j.get('cocktails'), parser.parse(time))
    guest.update_with_put('cocktails_excess', j.get('cocktails_excess'), parser.parse(time))

    Session.commit()

    return ''

# TODO: POST
# TODO: Marshallow
