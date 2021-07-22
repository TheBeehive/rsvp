from flask import Flask, request, make_response, abort, render_template
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from rsvp.database import Session, Guest, RSVP
from rsvp.resource import *
import json

app = Flask(__name__, static_url_path='/')

@app.route('/')
def welcome():
    return "<p>Welcome to Kai and Mel's RSVP. Use your URL to RSVP.</p>"

@app.errorhandler(404)
def handle_404(e):
    return app.send_static_file('404.html')

@app.errorhandler(NoResultFound)
def handle_no_result_found(exception):
    abort(404)

@app.route('/rsvp/<int:guest_id>')
def get_rsvp(guest_id):
    guest = Guest.query.filter_by(id=guest_id) \
        .options(joinedload(Guest.plus_one)) \
        .one()

    rsvp = RSVP.query.filter(RSVP.guest_id == guest_id) \
        .distinct(RSVP.guest_id) \
        .order_by(RSVP.guest_id, RSVP.submitted_at.desc()) \
        .one_or_none()

    rsvp_info = {
        'name': guest.name,
        'plusname': guest.plus_one.name if guest.plus_one else None,
        'email': guest.email,
        'invited_to_brunch': guest.invited_to_brunch,
    }
    if rsvp is not None:
        rsvp_info.update(RSVPSchema().dump(rsvp))
    print(rsvp_info)

    return render_template("index.html", rsvp_info=rsvp_info)

@app.route('/rsvp/<int:guest_id>', methods=['POST'])
def post_rsvp(guest_id):
    guest = Guest.query.filter_by(id=guest_id) \
            .with_for_update(read=False, key_share=True) \
            .one()
    rsvp = RSVP(guest=guest, **RSVPSchema().load(request.form))
    Session.add(rsvp)

    Session.commit()

    return ''
