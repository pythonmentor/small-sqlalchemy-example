from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)


def drop_and_create():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)