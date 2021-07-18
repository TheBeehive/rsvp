from flask import Flask
from flask import request, make_response, abort
from rsvp.database import *
from rsvp.resource import *
import json

app = Flask(__name__)

@app.route('/')
def welcome():
    return "<p>Welcome to Kai and Mel's RSVP. Use your URL to RSVP.</p>"

@app.route('/rsvp/<int:guest_id>')
def get_rsvp(guest_id):
    guest = Guest.query.get(guest_id)
    if guest is None:
        abort(404)

    response = {}

    plus_one = Guest.query.get(guest.plus_one) if guest.plus_one else None
    response['name'] = guest.name
    response['plus_one'] = plus_one.name if plus_one else None
    response['email'] = guest.email

    rsvp = RSVP.query.filter(RSVP.guest_id == guest_id) \
        .distinct(RSVP.guest_id) \
        .order_by(RSVP.guest_id, RSVP.submitted_at.desc()) \
        .one_or_none()

    response['cocktails'] = rsvp.cocktails if rsvp else None
    response['hike'] = rsvp.hike if rsvp else None
    response['wedding'] = rsvp.wedding if rsvp else None
    response['brunch'] = rsvp.brunch if rsvp else None

    return json.dumps(response)

@app.route('/rsvp/<int:guest_id>', methods=['POST'])
def post_rsvp(guest_id):
    guest = Guest.query.get(guest_id)
    if guest is None:
        abort(404)

    schema = RSVPSchema()
    rsvp_data = schema.load(request.form)
    rsvp_data['guest_id'] = guest_id

    rsvp = RSVP(**rsvp_data)

    Session.add(rsvp)
    Session.commit()

    return ''
