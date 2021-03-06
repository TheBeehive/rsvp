from sqlalchemy.orm import (
    declarative_base, relationship, sessionmaker, scoped_session)
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, FetchedValue,
    ForeignKey)
from sqlalchemy.dialects.postgresql import UUID

__all__ = ("Session", "Guest", "RSVP")

Base = declarative_base()
engine = create_engine('postgresql:///rsvp')
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(engine))


class Guest(Base):
    __tablename__ = 'guest'

    id = Column(Integer, primary_key=True, server_default=FetchedValue())
    name = Column(String, nullable=False, unique=True)
    nickname = Column(String, nullable=False)
    plus_one_id = Column(Integer, ForeignKey('guest.id'))
    email = Column(String, nullable=False)
    invited_to_brunch = Column(Boolean, nullable=False)
    secret_id = Column(UUID(as_uuid=True), nullable=False,
            server_default=FetchedValue())
    extension = Column(String)

    plus_one = relationship('Guest', remote_side=[id], post_update=True)
    rsvps = relationship('RSVP', back_populates='guest')

    query = Session.query_property()

    def __repr__(self):
        return f'<Guest id={self.id!r} name={self.name!r}>'

class RSVP(Base):
    __tablename__ = 'rsvp'

    id = Column(Integer, primary_key=True, server_default=FetchedValue())
    guest_id = Column(Integer, ForeignKey('guest.id'))

    wedding = Column(Boolean, nullable=False)
    diet_info = Column(String)
    vaxxed = Column(Boolean)
    masked = Column(Boolean)
    plusname = Column(String)
    plusvaxxed = Column(Boolean)
    plusmasked = Column(Boolean)

    cocktails = Column(Boolean)
    cocktails_excess = Column(Integer)
    pluscocktails = Column(Boolean)

    hike = Column(Boolean)
    phone = Column(String)
    plushike = Column(Boolean)
    plusphone = Column(String)

    brunch = Column(Boolean)
    plusbrunch = Column(Boolean)

    submitted_at = Column(Integer, nullable=False, server_default=FetchedValue())

    guest = relationship(Guest, back_populates='rsvps')

    query = Session.query_property()

    def __repr__(self):
        return f'<RSVP id={self.id!r} guest_id={self.guest_id!r}>'
