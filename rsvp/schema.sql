DROP TABLE IF EXISTS guest CASCADE;
CREATE TABLE guest (
  id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  name TEXT NOT NULL,
  plus_one INTEGER REFERENCES guest(id),
  email TEXT NOT NULL,
  invited_to_brunch BOOLEAN NOT NULL
);

DROP TABLE IF EXISTS rsvp CASCADE;
CREATE TABLE rsvp(
  id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  guest_id INTEGER NOT NULL REFERENCES guest(id),

  brunch BOOLEAN,

  wedding BOOLEAN NOT NULL,
  vaxxed BOOLEAN,
  CONSTRAINT vaccination_status CHECK (
    (wedding IS FALSE AND vaxxed IS NULL) OR
    (wedding IS TRUE AND vaxxed IS NOT NULL)
  ),
  masked BOOLEAN,
  CONSTRAINT masked_compliance CHECK (
    (vaxxed IS NULL AND masked IS NULL) OR
    (vaxxed IS TRUE AND masked IS NULL) OR
    (vaxxed IS FALSE AND masked IS TRUE)
  ),

  hike BOOLEAN NOT NULL,
  phone TEXT,
  CONSTRAINT hike_phone_provided CHECK (
    (hike IS FALSE AND phone IS NULL) OR
    (hike IS TRUE AND phone IS NOT NULL)
  ),

  cocktails BOOLEAN NOT NULL,
  cocktails_excess INTEGER,
  CONSTRAINT cocktails_excess_specified CHECK (
    (cocktails IS FALSE AND cocktails_excess IS NULL) OR
    (cocktails IS TRUE AND cocktails_excess IS NOT NULL)
  ),

  submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- TODO: interpolate guest name
CREATE OR REPLACE FUNCTION check_brunch_invitation() RETURNS TRIGGER AS $$
BEGIN
  IF
    NEW.brunch IS NOT NULL AND
    (SELECT invited_to_brunch FROM guest WHERE id = NEW.guest_id) IS FALSE
  THEN
    RAISE EXCEPTION 'Guest is not invited to brunch and thus cannot RSVP';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS brunch_validation ON rsvp;
CREATE TRIGGER brunch_validation
  BEFORE INSERT ON rsvp
  FOR EACH ROW
  EXECUTE FUNCTION check_brunch_invitation();
