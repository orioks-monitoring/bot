from sqlalchemy import Column, Integer, CheckConstraint

from app.models import BaseModel


class AdminStatistics(BaseModel):
    __tablename__ = 'admin_statistics'

    scheduled_requests = Column(Integer, nullable=False, default=0)
    success_logins = Column(Integer, nullable=False, default=0)
    failed_logins = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        CheckConstraint(
            scheduled_requests >= 0,
            name='check_scheduled_requests_non_negative',
        ),
        CheckConstraint(
            success_logins >= 0, name='check_success_logins_non_negative'
        ),
        CheckConstraint(
            failed_logins >= 0, name='check_failed_logins_non_negative'
        ),
        {},
    )

    def fill(
        self, scheduled_requests: int, success_logins: int, failed_logins: int
    ):
        self.scheduled_requests = scheduled_requests
        self.success_logins = success_logins
        self.failed_logins = failed_logins
