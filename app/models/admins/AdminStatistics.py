from sqlalchemy import Column, Integer

from app.models import BaseModel


class AdminStatistics(BaseModel):
    __tablename__ = 'admin_statistics'

    scheduled_requests = Column(Integer, nullable=False, default=0)
    success_logins = Column(Integer, nullable=False, default=0)
    failed_logins = Column(Integer, nullable=False, default=0)

    def fill(
        self, scheduled_requests: int, success_logins: int, failed_logins: int
    ):
        self.scheduled_requests = scheduled_requests
        self.success_logins = success_logins
        self.failed_logins = failed_logins
