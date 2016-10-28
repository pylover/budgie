
from datetime import datetime

from sqlalchemy import Unicode, Column, Integer, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from budgie.configuration import settings

Base = declarative_base()

DBSession = scoped_session(sessionmaker())
Base.query = DBSession.query_property()
metadata = Base.metadata
engine = None


class Workstation(Base):
    __tablename__ = 'workstation'

    id = Column(Integer, primary_key=True)
    host_name = Column(Unicode(50), nullable=False)
    entry_time = Column(DateTime, nullable=False, default=datetime.now())
    memory = Column(Integer, nullable=True)
    cpu_usages = Column(Integer)  # For now , just average of all available cores is stored.


def init():
    global engine
    engine = create_engine(settings.db.uri, echo=settings.db.echo)
    DBSession.configure(bind=engine)


def create_database_objects(cli_arguments):
    print('Creating Database schema')
    init()
    metadata.create_all(engine, checkfirst=True)

    print('done')
