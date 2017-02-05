
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, DateTime, Column, String, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import JSONB

import settings
import datetime

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

class ScrapItem(DeclarativeBase):
    """Sqlalchemy scrap item model"""
    __tablename__ = "scrap_items"

    id = Column(String, primary_key=True, autoincrement=False)
    doc = Column('doc', JSONB)
    kind = Column('kind', String)
    updated_at = Column('updated_at', DateTime, default=datetime.datetime.now)

