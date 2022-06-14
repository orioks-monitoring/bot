from sqlalchemy import Column, Integer, Boolean

from app.models import BaseModel


class UserStatus(BaseModel):

    __tablename__ = 'user_status'

    user_telegram_id = Column(Integer, nullable=False)
    agreement_accepted = Column(Boolean, nullable=False, default=False)
    authenticated = Column(Boolean, nullable=False, default=False)
    login_attempt_count = Column(Integer, nullable=False, default=0)

    def fill(self, user_telegram_id: int):
        self.user_telegram_id = user_telegram_id
        self.agreement_accepted = False
        self.authenticated = False
        self.login_attempt_count = 0
