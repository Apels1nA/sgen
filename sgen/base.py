from abc import ABC, abstractmethod
from typing import List, Any


class ValidatorABC(ABC):
    @abstractmethod
    def positive(self, data_type) -> List[Any]:
        """
        Generates positive values for a field according to validation parameters

        :param data_type: Object of a concrete data type class (field)
        :type data_type: Field
        """

        pass

    @abstractmethod
    def negative(self, data_type) -> List[Any]:
        """
        Generates negative values for a field according to validation parameters

        :param data_type: Object of a concrete data type class (field)
        :type data_type: Field
        """

        pass
