#! /usr/bin/env python3

from rsvp.database import Guest, Session
import subprocess
import sys
import textwrap

for guest in Session.query(Guest).order_by(Guest.name):
    subject = "You're invited to Kaiting + Melanie's Wedding"
    recipient = 'ktchen14@gmail.com'
    # recipient = guest.email

    link = f'https://rsvp.hackersgethitched.com/rsvp/{guest.secret_id}'
    template = textwrap.dedent(f"""
        {guest.nickname},

        You're invited to join us at our wedding on October 23rd, 2021, at the Computer History Museum in Mountain View, CA.

        As a reminder, the most up to date information on the event is available on our wedding website at https://hackersgethitched.com.

        Please RSVP by September 15th, 2021, using your personalized RSVP form at:

        {link}

        Note that only submissions using this form will be recorded in our wedding attendance database.

        -- Kaiting + Melanie
    """)

    print(f'Sending invitation to {guest.name} <{guest.email}> ...',
          file=sys.stderr)
    try:
        subprocess.run([
            'mutt', '-s', subject, recipient, '-e', 'set copy=no',
        ], check=True, input=template, text=True)
    except subprocess.CalledProcessError as e:
        print(f'Failed ({e})', file=sys.stderr)
        continue
    print('Success\n', file=sys.stderr)
