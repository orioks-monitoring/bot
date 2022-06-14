from sqlalchemy import Column, Integer, Boolean

from app.models import BaseModel


class UserNotifySettings(BaseModel):

    __tablename__ = 'user_notify_settings'

    user_telegram_id = Column(Integer, nullable=False)
    marks = Column(Boolean, nullable=False, default=True)
    news = Column(Boolean, nullable=False, default=True)
    discipline_sources = Column(Boolean, nullable=False, default=True)
    homeworks = Column(Boolean, nullable=False, default=True)
    requests = Column(Boolean, nullable=False, default=True)

    def fill(self, user_telegram_id: int) -> None:
        self.user_telegram_id = user_telegram_id
        self.marks = True
        self.news = True
        self.discipline_sources = True
        self.homeworks = True
        self.requests = True
