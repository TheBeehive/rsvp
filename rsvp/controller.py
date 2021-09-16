from flask import Flask, flash, get_flashed_messages, request, make_response, \
    abort, redirect, render_template, url_for
from marshmallow import EXCLUDE
from rsvp.database import Session, Guest, RSVP
from rsvp.resource import RSVPSchema, IndeterminateRSVPSchema
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
import os

root = os.path.realpath(os.path.join(__file__, '..', '..'))
app = Flask(__name__, static_url_path='/', root_path=root)
app.secret_key = 'This is very secret'
upload_folder = os.path.join(app.static_folder, 'upload')

ACCEPTED_UPLOAD_EXTENSION = (
    '.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi',  # JPEG
    '.png',                                            # PNG
    '.webp',                                           # WEBP
    '.tiff', '.tif',                                   # TIFF
    '.heif', '.heic',                                  # HEIF
    '.jp2', '.j2k', '.jpf', '.jpx', '.jpm', '.mj2',    # JPEG 2000
    '.pdf',                                            # PDF
)

@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove()

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

    ### Form Closed ###
    wedding = rsvp is not None and rsvp.wedding
    return render_template('gone.html', wedding=wedding), 410
    ### Form Closed ###

    rsvp_info = {
        'secret_id': guest.secret_id,
        'name': guest.name,
        'email': guest.email,
        'noods': guest.invited_to_brunch,
    }

    if guest.plus_one_id is not None:
        rsvp_info['type'] = 'rsvp'
        rsvp_info['plusname'] = guest.plus_one.name
        schema = RSVPSchema()
    else:
        rsvp_info['type'] = 'indeterminate_rsvp'
        schema = IndeterminateRSVPSchema()

    if rsvp is not None:
        rsvp_info.update(schema.dump(rsvp))

    return render_template("index.html", rsvp_info=rsvp_info)

@app.route('/rsvp/<uuid:secret_id>', methods=['POST'])
def post_rsvp(secret_id):
    guest = Guest.query.filter_by(secret_id=secret_id) \
            .one()

    ### Form Closed ###
    rsvp = RSVP.query.filter(RSVP.guest_id == guest.id) \
        .distinct(RSVP.guest_id) \
        .order_by(RSVP.guest_id, RSVP.submitted_at.desc()) \
        .one_or_none()

    wedding = rsvp is not None and rsvp.wedding
    return render_template('gone.html', wedding=wedding), 410
    ### Form Closed ###

    # .with_for_update(read=False, key_share=True) \

    if guest.plus_one_id is not None:
        schema = RSVPSchema(unknown=EXCLUDE)
    else:
        schema = IndeterminateRSVPSchema(unknown=EXCLUDE)

    rsvp = RSVP(guest=guest, **schema.load(request.form))
    Session.add(rsvp)

    Session.commit()

    rsvp_info = {
        'secret_id': guest.secret_id,
        'name': guest.name,
        'email': guest.email,
        'noods': guest.invited_to_brunch,
    }

    if guest.plus_one_id is not None:
        rsvp_info['type'] = 'rsvp'
        rsvp_info['plusname'] = guest.plus_one.name
    else:
        rsvp_info['type'] = 'indeterminate_rsvp'

    if rsvp is not None:
        rsvp_info.update(schema.dump(rsvp))

    return render_template("index.html", rsvp_info=rsvp_info)

@app.route('/vaxx/<uuid:secret_id>')
def get_vaxx(secret_id):
    guest = Guest.query.filter_by(secret_id=secret_id).one()
    vaxx_info = { 'name': guest.name }

    statuses = get_flashed_messages(category_filter=('status',))
    if statuses:
        vaxx_info['status'] = ', '.join(statuses)

    if guest.extension is not None:
        path = os.path.join('upload', f'{guest.name}.{guest.extension}')
        vaxx_info['on_server'] = url_for('static', filename=path)

    return render_template("vaxx.html", vaxx_info=vaxx_info)

@app.route('/vaxx/<uuid:secret_id>', methods=['POST'])
def post_vaxx(secret_id):
    guest = Guest.query.filter_by(secret_id=secret_id).one()
    vaxx_info = { 'name': guest.name }

    if guest.extension is not None:
        path = os.path.join('upload', f'{guest.name}.{guest.extension}')
        vaxx_info['on_server'] = url_for('static', filename=path)

    file = request.files.get('file')

    if file is None or file.filename == '':
        vaxx_info['error'] = 'No file uploaded on form submission'
        return render_template("vaxx.html", vaxx_info=vaxx_info)

    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ACCEPTED_UPLOAD_EXTENSION:
        vaxx_info['error'] = f"Can't accept file with extension {extension}"
        return render_template("vaxx.html", vaxx_info=vaxx_info)
    extension = extension[1:]

    file.save(os.path.join(upload_folder, f'{guest.name}.{extension}'))

    guest.extension = extension
    Session.commit()

    flash('Upload succeeded', category='status')
    return redirect(url_for('get_vaxx', secret_id=secret_id), code=303)
