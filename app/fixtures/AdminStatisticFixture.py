from app.fixtures import AbstractFixture
from app.models.admins import AdminStatistics


class AdminStatisticFixture(AbstractFixture):
    model = AdminStatistics
    values = [
        {'scheduled_requests': 0, 'success_logins': 0, 'failed_logins': 0}
    ]
