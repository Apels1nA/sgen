from typing import Any, List


def has_data_type(values: List[Any], data_type: Any) -> bool:
    """
    Проверяет наличие data_type в values

    :return: True если data_type в values
    """

    return bool(list(filter(
        lambda value: isinstance(value, data_type),
        values
    )))


class Unique:
    """Представляет уникальное значение для использования в тестах"""

    last_index = 0

    def __new__(cls):
        cls.last_index += 1
        instance = super().__new__(cls)
        return instance

    def __init__(self):
        self.index = self.last_index

    def __repr__(self):
        return f"<Unique:{self.index}>"
