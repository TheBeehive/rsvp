from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, FetchedValue

Base = declarative_base()
engine = create_engine('postgresql:///rsvp')
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(engine))

class Guest(Base):
    __tablename__ = 'guest'

    id = Column(Integer, primary_key=True,
                      server_default=FetchedValue())
    name = Column(String)
    plus_one = Column(Integer)
    email = Column(String, nullable=False)
    invited_to_brunch = Column(Boolean, nullable=False)

    query = Session.query_property()

    def __repr__(self):
        return f'<Guest guest_id={self.id!r}, name={self.name!r}>'

class RSVP(Base):
    __tablename__ = 'rsvp'

    id = Column(Integer, primary_key=True,
                      server_default=FetchedValue())

    guest_id = Column(Integer)
    brunch = Column(Boolean)
    wedding = Column(Boolean, nullable=False)
    vaxxed = Column(Boolean)
    masked = Column(Boolean)
    hike = Column(Boolean, nullable=False)
    phone = Column(String)
    cocktails = Column(Boolean, nullable=False)
    cocktails_excess = Column(Integer)

    submitted_at = Column(Integer, server_default=FetchedValue())

    query = Session.query_property()

    def __repr__(self):
        return f'<RSVP id={self.id!r}, guest_id={self.guest_id!r}>'
