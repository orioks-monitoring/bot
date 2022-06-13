from sqlalchemy import Column, Integer

from app.models import BaseModel


class AdminStatistics(BaseModel):

    scheduled_requests = Column(Integer, nullable=False, default=0)
    success_logins = Column(Integer, nullable=False, default=0)
    failed_logins = Column(Integer, nullable=False, default=0)
