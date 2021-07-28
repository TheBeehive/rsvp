from flask import Flask, request, make_response, abort, render_template
from marshmallow import EXCLUDE
from rsvp.database import Session, Guest, RSVP
from rsvp.resource import RSVPSchema
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
import os

root = os.path.realpath(os.path.join(__file__, '..', '..'))
app = Flask(__name__, static_url_path='/', root_path=root)

@app.errorhandler(404)
def handle_404(e):
    return app.send_static_file('404.html'), 404

@app.errorhandler(NoResultFound)
def handle_no_result_found(exception):
    return app.send_static_file('404.html'), 404

@app.route('/rsvp/<uuid:secret_id>')
def get_rsvp(secret_id):
    guest = Guest.query.filter_by(secret_id=secret_id) \
        .options(joinedload(Guest.plus_one)) \
        .one()

    rsvp = RSVP.query.filter(RSVP.guest_id == guest.id) \
        .distinct(RSVP.guest_id) \
        .order_by(RSVP.guest_id, RSVP.submitted_at.desc()) \
        .one_or_none()

    rsvp_info = {
        'secret_id': guest.secret_id,
        'name': guest.name,
        'plusname': guest.plus_one.name if guest.plus_one else None,
        'email': guest.email,
        'invited_to_brunch': guest.invited_to_brunch,
    }
    if rsvp is not None:
        rsvp_info.update(RSVPSchema().dump(rsvp))

    return render_template("index.html", rsvp_info=rsvp_info)

@app.route('/rsvp/<uuid:secret_id>', methods=['POST'])
def post_rsvp(secret_id):
    schema = RSVPSchema(unknown=EXCLUDE)

    guest = Guest.query.filter_by(secret_id=secret_id) \
            .with_for_update(read=False, key_share=True) \
            .one()
    rsvp = RSVP(guest=guest, **schema.load(request.form))
    Session.add(rsvp)

    Session.commit()

    rsvp_info = {
        'secret_id': guest.secret_id,
        'name': guest.name,
        'plusname': guest.plus_one.name if guest.plus_one else None,
        'email': guest.email,
        'invited_to_brunch': guest.invited_to_brunch,
    }
    rsvp_info.update(schema.dump(rsvp))

    return render_template("index.html", rsvp_info=rsvp_info)
