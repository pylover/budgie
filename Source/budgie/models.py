"""
All database stuff will be done here.

I use the code-first method, for using ORM's

"""

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


class AgentLog(Base):
    """
    The only model of this applcation.
    it holds the log of observation agent.
    """
    __tablename__ = 'agent_log'

    id = Column(Integer, primary_key=True)
    hostname = Column(Unicode(50), nullable=False)
    entry_time = Column(DateTime, nullable=False, default=datetime.now())
    end_time = Column(DateTime, nullable=True)
    error = Column(Unicode(1024), nullable=True)
    memory = Column(Integer, nullable=True)
    cpu = Column(Integer)  # For now , just average of all available cores is stored.


def init():
    """
    Initialize the mapper and binding configurations.

    """
    global engine
    engine = create_engine(settings.db.uri, echo=settings.db.echo)
    metadata.bind = engine
    DBSession.configure(bind=engine)


def create_database_objects(cli_arguments):
    """
    Generates the database objects.

    """
    print('Creating Database schema')
    init()
    metadata.create_all(engine, checkfirst=True)
    print('done')
