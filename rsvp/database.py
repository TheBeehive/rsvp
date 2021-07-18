from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, FetchedValue

Base = declarative_base()
engine = create_engine('postgresql:///rsvp')
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(engine))

class RSVP(Base):
    __tablename__ = 'rsvp'

    guest_id = Column(Integer, primary_key=True,
                      server_default=FetchedValue())
    guest_name = Column(String)
    plus_one = Column(Integer)
    email = Column(String)
    invited_to_brunch = Column(Boolean)
    brunch = Column(String)
    brunch_time = Column(String)
    wedding = Column(String)
    wedding_time = Column(String)
    vaxxed = Column(String)
    vaxxed_time = Column(String)
    masked = Column(String)
    masked_time = Column(String)
    hike = Column(String)
    hike_time = Column(String)
    phone = Column(String)
    phone_time = Column(String)
    cocktails = Column(String)
    cocktails_time = Column(String)
    cocktails_excess = Column(String)
    cocktails_excess_time = Column(String)

    query = Session.query_property()

    def __repr__(self):
        return f'<RSVP guest_id={self.guest_id!r}, guest_name={self.guest_name!r}>'

    def update_with_put(self, field, update_value, update_time):
        if update_value is None:
            return

        current_value = getattr(self, field)
        current_value_time = getattr(self, field + '_time')

        if current_value is None:
            assert(current_value_time is None)
            setattr(self, field, update_value)
            setattr(self, field + '_time', update_value_time)

        else:
            assert(current_value_time is not None)
            if current_value_time < update_time:
                setattr(self, field, update_value)
                setattr(self, field + '_time', update_value_time)
