from .AbstractFixture import AbstractFixture
from .AdminStatisticFixture import AdminStatisticFixture

__all__ = ['AbstractFixture', 'AdminStatisticFixture']


def initialize_default_values():
    fixture_classes = [AdminStatisticFixture]
    for fixture_class in fixture_classes:
        fixture_class = fixture_class()
        fixture_class.insert_data()
