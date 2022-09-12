from abc import abstractmethod
from typing import Type

from app.models import BaseModel


class AbstractFixture:
    @property
    @abstractmethod
    def model(self) -> Type[BaseModel]:
        raise NotImplementedError

    @property
    def fill_method_name(self) -> str:
        return 'fill'

    @abstractmethod
    def values(self) -> list[dict]:
        raise NotImplementedError

    def need_to_add_values(self) -> bool:
        items_count = self.model.query.count()
        if items_count > 0:
            return False
        return True

    def insert_data(self) -> bool:
        if not self.need_to_add_values():
            return False

        values = self.values() if callable(self.values) else self.values

        for value in values:
            model = self.model()
            getattr(model, self.fill_method_name)(**value)
            model.save()
        return True
