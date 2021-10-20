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

result = [rsvp for rsvp in result if rsvp.wedding]
result = [rsvp for rsvp in result if rsvp.guest.name != 'Francis Shirekuli']

nobrunch_result = [rsvp for rsvp in result if not rsvp.brunch]
brunch_result = [rsvp for rsvp in result if rsvp.brunch]

for rsvp in nobrunch_result:
    subject = 'Last Wedding Update!'
    # recipient = 'ktchen14@gmail.com'
    recipient = rsvp.guest.email

    link = f'https://rsvp.hackersgethitched.com/vaxx/{rsvp.guest.secret_id}'
    template = textwrap.dedent(f"""
        <p>Hi everyone. The wedding’s less than a week away and we can’t wait
        to see you! Please read this email <strong>in full</strong> as we have
        a number of important updates. As a reminder, the latest information is
        always on our wedding website at:</p>

        <p><a href="https://hackersgethitched.com/">https://hackersgethitched.com/</a></p>

        <h2>Wedding Time Change</h2>

        <p>The wedding has been moved up by half an hour. It now starts at
        05:00 PM and will last until midnight. The Lyft code <a
        href="https://www.lyft.com/i/KAIMEL4EVER">KAIMEL4EVER</a> is available
        to get you to and from the museum.</p>

        <h2>COVID-19 Protocol</h2>

        <p>Masks will no longer be required at the wedding on Saturday, October
        23rd (they’re still required at Friday’s welcome reception). Through an
        attorney, we’ve received clarification from Santa Clara County that our
        wedding will be exempt from the mask ordinance. To keep everyone safe,
        we’ve instituted a number of changes:</p>

        <ol style="padding-left: 0px;">
            <li><p>COVID-19 rapid tests will be available before entrance into
            the event. We ask that you take a rapid test and confirm a negative
            result before entering if: <ol type=a style="padding-left: 0px;">
                <li>You have any symptoms of COVID-19, or</li>
                <li>You have been, or will have been, in contact with someone
                with a confirmed case of COVID-19 within 14 days of the
                wedding.</li>
            </ol></p></li>

            <li><p>Social distancing bracelets will be offered. Please wear a
            bracelet to indicate that you’d like others to maintain a
            respectful distance from you and to wear a mask around you whenever
            possible. In addition, we ask all guests to pay attention and
            respect the wishes of anyone wearing a social distancing bracelet
            (please <strong>bring a mask</strong> to the wedding).</p></li>

            <li>
                <p>Demonstrable proof of vaccination is a requirement for
                entrance into the wedding. All staff at the event will be
                vaccinated. And if you haven’t already done so, please upload
                your proof of vaccination at:</p>

                <p><a href="{link}">{link}</a></p>

                <p>Before Thursday, October 21st. If you haven’t done this by
                that time, then you <strong>must</strong> bring your proof of
                vaccination and a photo ID to the wedding. Otherwise you
                <strong>will</strong> be refused admission into the event.
            </li>
        </ol>

        <p>Please note that all applicable COVID-19 local regulations apply
        before and after the wedding. The mask exemption is only for events
        occurring at the Computer History Museum directly associated with our
        wedding. For example, if you take a Lyft to the wedding, you must wear
        a mask in the Lyft.</p>
    """)

    print(f'Sending message to {rsvp.guest.name} <{rsvp.guest.email}> ...',
          file=sys.stderr)
    try:
        subprocess.run([
            'mutt', '-s', subject, recipient, '-e', 'set copy=no',
            '-e', 'set content_type=text/html',
        ], check=True, input=template, text=True)
    except subprocess.CalledProcessError as e:
        print(f'Failed ({e})', file=sys.stderr)
        continue
    print('Success\n', file=sys.stderr)

for rsvp in brunch_result:
    subject = 'Last Wedding Update!'
    # recipient = 'ktchen14@gmail.com'
    recipient = rsvp.guest.email

    link = f'https://rsvp.hackersgethitched.com/vaxx/{rsvp.guest.secret_id}'
    template = textwrap.dedent(f"""
        <p>Hi everyone. The wedding’s less than a week away and we can’t wait
        to see you! Please read this email <strong>in full</strong> as we have
        a number of important updates. As a reminder, the latest information is
        always on our wedding website at:</p>

        <p><a href="https://hackersgethitched.com/">https://hackersgethitched.com/</a></p>

        <h2>Wedding Time Change</h2>

        <p>The wedding has been moved up by half an hour. It now starts at
        05:00 PM and will last until midnight. The Lyft code <a
        href="https://www.lyft.com/i/KAIMEL4EVER">KAIMEL4EVER</a> is available
        to get you to and from the museum.</p>

        <h2>COVID-19 Protocol</h2>

        <p>Masks will no longer be required at the wedding on Saturday, October
        23rd (they’re still required at Friday’s welcome reception and Sunday's
        brunch). Through an attorney, we’ve received clarification from Santa
        Clara County that our wedding will be exempt from the mask ordinance.
        To keep everyone safe, we’ve instituted a number of changes:</p>

        <ol style="padding-left: 0px;">
            <li><p>COVID-19 rapid tests will be available before entrance into
            the event. We ask that you take a rapid test and confirm a negative
            result before entering if: <ol type=a style="padding-left: 0px;">
                <li>You have any symptoms of COVID-19, or</li>
                <li>You have been, or will have been, in contact with someone
                with a confirmed case of COVID-19 within 14 days of the
                wedding.</li>
            </ol></p></li>

            <li><p>Social distancing bracelets will be offered. Please wear a
            bracelet to indicate that you’d like others to maintain a
            respectful distance from you and to wear a mask around you whenever
            possible. In addition, we ask all guests to pay attention and
            respect the wishes of anyone wearing a social distancing bracelet
            (please <strong>bring a mask</strong> to the wedding).</p></li>

            <li>
                <p>Demonstrable proof of vaccination is a requirement for
                entrance into the wedding. All staff at the event will be
                vaccinated. And if you haven’t already done so, please upload
                your proof of vaccination at:</p>

                <p><a href="{link}">{link}</a></p>

                <p>Before Thursday, October 21st. If you haven’t done this by
                that time, then you <strong>must</strong> bring your proof of
                vaccination and a photo ID to the wedding. Otherwise you
                <strong>will</strong> be refused admission into the event.
            </li>
        </ol>

        <p>Please note that all applicable COVID-19 local regulations apply
        before and after the wedding. The mask exemption is only for events
        occurring at the Computer History Museum directly associated with our
        wedding. For example, if you take a Lyft to the wedding, you must wear
        a mask in the Lyft.</p>

        <h2>Brunch</h2>

        <p>The restaurant where we were planning on hosting brunch, Chang’an
        Artisan Noodle, is unfortunately closing. As a result, brunch has been
        moved to <a href="https://g.page/daigo-palo-alto?share">Daigo</a> in
        Palo Alto and will commence at noon.</p>
    """)

    print(f'Sending message to {rsvp.guest.name} <{rsvp.guest.email}> ...',
          file=sys.stderr)
    try:
        subprocess.run([
            'mutt', '-s', subject, recipient, '-e', 'set copy=no',
            '-e', 'set content_type=text/html',
        ], check=True, input=template, text=True)
    except subprocess.CalledProcessError as e:
        print(f'Failed ({e})', file=sys.stderr)
        continue
    print('Success\n', file=sys.stderr)
