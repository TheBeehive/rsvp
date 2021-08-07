DROP TABLE IF EXISTS guest CASCADE;
CREATE TABLE guest (
  id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  name TEXT NOT NULL UNIQUE,
  nickname TEXT NOT NULL,
  plus_one_id INTEGER REFERENCES guest(id),
  email TEXT NOT NULL,
  invited_to_brunch BOOLEAN NOT NULL,
  secret_id UUID NOT NULL UNIQUE DEFAULT gen_random_uuid()
);

DROP TABLE IF EXISTS rsvp CASCADE;
CREATE TABLE rsvp (
  id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  guest_id INTEGER NOT NULL REFERENCES guest(id),

  wedding BOOLEAN NOT NULL,
  vaxxed BOOLEAN,
  masked BOOLEAN,
  plusname TEXT CHECK (plusname != ''),
  plusvaxxed BOOLEAN,
  plusmasked BOOLEAN,

  cocktails BOOLEAN,
  cocktails_excess INTEGER,
  pluscocktails BOOLEAN,

  hike BOOLEAN,
  phone TEXT CHECK (phone != ''),
  plushike BOOLEAN,
  plusphone TEXT CHECK (plusphone != ''),

  brunch BOOLEAN,
  plusbrunch BOOLEAN,

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
