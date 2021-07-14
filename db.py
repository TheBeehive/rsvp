import psycopg2

connection = psycopg2.connect(
    dbname='rsvp'
)
def do_rsvp(guest_id, event_id, value):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO rsvp(guest_id, event_id, value) VALUES (%s, %s, %s)", (guest_id, event_id, value))
        connection.commit()

        cursor.execute('SELECT * FROM rsvp')
        for record in cursor:
            print(record)
