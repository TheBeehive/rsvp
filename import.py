#! /usr/bin/env python3

from csv import DictReader
from rsvp.database import Guest, Session
from sqlalchemy.dialects.postgresql import insert
import os

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_ROOT = os.path.join(SCRIPT_ROOT, 'data')

path = os.path.join(DATA_ROOT, 'main.csv')
with open(path, encoding='utf-8-sig') as file:
    reader = DictReader(file)
    for person in reader:
        if person['LAST NAME'] == 'Plus One':
            continue

        name = f"{person['NAME']} {person['LAST NAME']}"
        mail = person['E-MAIL']
        nickname = person['NAME']

        insert_stmt = insert(Guest).values(
                name=name, email=mail, nickname=nickname)
        update_stmt = insert_stmt.on_conflict_do_update(
            set_={
                'email': insert_stmt.excluded.email,
                'nickname': insert_stmt.excluded.nickname,
            }, index_elements=(Guest.name,))
        Session.execute(update_stmt)

path = os.path.join(DATA_ROOT, 'nickname.csv')
with open(path, encoding='utf-8-sig') as file:
    reader = DictReader(file)
    for person in reader:
        record = Session.query(Guest).filter_by(name=person['name']).one()
        record.nickname = person['nickname']

path = os.path.join(DATA_ROOT, 'brunch.csv')
with open(path, encoding='utf-8-sig') as file:
    reader = DictReader(file)
    for person in reader:
        if person['LAST NAME'] == 'Plus One':
            continue
        name = f"{person['NAME']} {person['LAST NAME']}"
        record = Session.query(Guest).filter_by(name=name).one()
        record.invited_to_brunch = True

path = os.path.join(DATA_ROOT, 'plus_ones.csv')
with open(path, encoding='utf-8-sig') as file:
    reader = DictReader(file) 
    for pair in reader:
        guest = Session.query(Guest).filter_by(name=pair['name']).one()

        if not pair['plus_one']:
            guest.plus_one = None
        else:
            plus_one = Session.query(Guest).filter_by(name=pair['plus_one']).one()
            guest.plus_one = plus_one
            plus_one.plus_one = guest

Session.commit()

# # send email
# for f in os.listdir('myspecialdir'):
#     subject = "You're invited to Kaiting + Melanie's Wedding"
#     email = os.path.basename(f)
#     filename = os.path.abspath(f)
#     mutt_command = f"mutt -s {subject} {email} < {filename}"
#     subprocess.run(mutt_command)
