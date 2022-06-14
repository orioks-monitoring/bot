from sqlalchemy import Column, DateTime, func, Integer

from app import db_session
from app.models import DeclarativeModelBase


class BaseModel(DeclarativeModelBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @classmethod
    def find_one(cls, **query):
        return cls.query.filter_by(**query).one_or_none()

    def save(self):
        if self.id is None:
            db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def as_dict(self):
        return {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
