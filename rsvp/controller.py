from flask import Flask
from flask import request, make_response, abort
from sqlalchemy.orm.exc import NoResultFound
from rsvp.database import *
from rsvp.resource import *
import json

app = Flask(__name__)

@app.route('/')
def welcome():
    return "<p>Welcome to Kai and Mel's RSVP. Use your URL to RSVP.</p>"

@app.errorhandler(NoResultFound)
def handle_no_result_found(exception):
    return 'No guest with that id found', 404

@app.route('/rsvp/<int:guest_id>')
@retrieve_guest
def get_rsvp(guest):
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
@retrieve_guest
def post_rsvp(guest):
    schema = RSVPSchema()
    rsvp_data = schema.load(request.form)
    rsvp_data['guest_id'] = guest_id

    rsvp = RSVP(**rsvp_data)

    Session.add(rsvp)
    Session.commit()

    return ''
