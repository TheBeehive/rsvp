#! /usr/bin/env python3

from sqlalchemy.orm import joinedload
from rsvp.database import Guest, RSVP, Session
import subprocess
import sys
import textwrap

result = Session.query(RSVP).distinct(RSVP.guest_id). \
        options(joinedload(RSVP.guest)). \
        order_by(RSVP.guest_id, RSVP.submitted_at.desc()). \
        all()

for rsvp in result:
    if not rsvp.wedding:
        continue

    subject = 'Proof of Vaccination Upload'
    # recipient = 'ktchen14@gmail.com'
    recipient = rsvp.guest.email

    link = f'https://rsvp.hackersgethitched.com/vaxx/{rsvp.guest.secret_id}'
    template = textwrap.dedent(f"""
        {rsvp.guest.nickname},

        Thank you for RSVP'ing to our wedding! We're very excited to see you soon. To ensure the safety of all participants, we are requiring that all guests and staff be fully vaccinated*.

        So that the day runs smoothly, we are requiring participants to provide proof of full vaccination prior to the wedding. Please upload your proof of vaccination using this personalized link:

        {link}

        *For our purposes, a US resident is considered fully vaccinated after receiving either 1) one dose of Johnson & Johnson's Janssen 2) two doses of Moderna's Spikevax or 3) two doses of Pfizer-BioNTech's Comirnaty.

        As a reminder, the most up to date information on the event is available on our wedding website at https://hackersgethitched.com/.

        -- Kaiting + Melanie
    """)

    print(f'Sending message to {rsvp.guest.name} <{rsvp.guest.email}> ...',
          file=sys.stderr)
    try:
        subprocess.run([
            'mutt', '-s', subject, recipient, '-e', 'set copy=no',
        ], check=True, input=template, text=True)
    except subprocess.CalledProcessError as e:
        print(f'Failed ({e})', file=sys.stderr)
        continue
    print('Success\n', file=sys.stderr)
