from sqlalchemy.orm import declarative_base, scoped_session

from .. import db_session

session = scoped_session(db_session)
DeclarativeModelBase = declarative_base()
DeclarativeModelBase.query = session.query_property()
from .BaseModel import BaseModel

__all__ = ['DeclarativeModelBase', 'BaseModel']
