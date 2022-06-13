from sqlalchemy.orm import declarative_base

DeclarativeModelBase = declarative_base()

from .BaseModel import BaseModel

__all__ = ['DeclarativeModelBase', 'BaseModel']
