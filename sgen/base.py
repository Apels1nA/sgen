from abc import ABC, abstractmethod
from typing import List, Any


class FieldABC(ABC):
    @abstractmethod
    def positive(self):
        pass

    @abstractmethod
    def negative(self):
        pass

    @abstractmethod
    def get_other_value(self, value: Any):
        pass


class ValidatorABC:
    @abstractmethod
    def positive(self, data_type: FieldABC) -> List[Any]:
        pass

    @abstractmethod
    def negative(self, data_type: FieldABC) -> List[Any]:
        pass
