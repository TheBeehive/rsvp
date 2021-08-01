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

    plus_one = relationship('Guest', remote_side=[id])
    rsvps = relationship('RSVP', back_populates='guest')

    query = Session.query_property()

    def __repr__(self):
        return f'<Guest id={self.id!r} name={self.name!r}>'

class RSVP(Base):
    __tablename__ = 'rsvp'

    id = Column(Integer, primary_key=True, server_default=FetchedValue())
    guest_id = Column(Integer, ForeignKey('guest.id'))
    brunch = Column(Boolean)
    wedding = Column(Boolean, nullable=False)
    vaxxed = Column(Boolean)
    masked = Column(Boolean)
    hike = Column(Boolean, nullable=False)
    phone = Column(String)
    cocktails = Column(Boolean, nullable=False)
    cocktails_excess = Column(Integer)
    submitted_at = Column(Integer, server_default=FetchedValue())

    guest = relationship(Guest, back_populates='rsvps')

    query = Session.query_property()

    def __repr__(self):
        return f'<RSVP id={self.id!r} guest_id={self.guest_id!r}>'
