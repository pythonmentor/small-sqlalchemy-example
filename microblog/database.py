"""Module responsible of establishing the connection with the database and 
creating a session class for this connection."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)


def drop_and_create():
    """Drops all the tables (if any) in the database and creates them again."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)