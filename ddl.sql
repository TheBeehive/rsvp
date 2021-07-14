DROP TABLE IF EXISTS guest CASCADE;
CREATE TABLE guest (
  id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, 
  name TEXT
);

DROP TABLE IF EXISTS event CASCADE;
CREATE TABLE event (
  id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  name TEXT
);

DROP TABLE IF EXISTS rsvp;
CREATE TABLE rsvp(
  id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  value TEXT NOT NULL,
  event_id INTEGER REFERENCES event(id) ON DELETE CASCADE,
  guest_id INTEGER REFERENCES guest(id) ON DELETE CASCADE
);
