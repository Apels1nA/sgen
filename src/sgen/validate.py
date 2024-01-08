from typing import List, Any, Union
from datetime import datetime, date

from sgen.base import ValidatorABC
from sgen.fields import Float, Field


__all__ = [
    "Length",
    "Range",
    "Equal",
    "OneOf",
    "NoneOf",
]


class Length(ValidatorABC):
    """Limits the length of a collection"""

    def __init__(
            self,
            min: int = None,
            max: int = None,
            min_inclusive: bool = True,
            max_inclusive: bool = True,
    ):
        """
        Initializes the validator

        :param min: Minimum length.
        :param max: Maximum length.
        :param min_inclusive: True if min is a valid list length
        :param max_inclusive: True if max is a valid list length
        """

        if not min and not max:
            raise ValueError("One of the parameters min, max is required")

        if isinstance(min, int) and isinstance(max, int):
            min_ = min if min_inclusive else min + 1
            max_ = max if max_inclusive else max - 1

            if min_ >= max_:
                raise ValueError("The minimum value cannot be greater than or equal to the maximum")

        self.min = min
        self.max = max
        if isinstance(min, int):
            self.min = min if min_inclusive else min + 1
        if isinstance(max, int):
            self.max = max if max_inclusive else max - 1

    def positive(self, data_type: Field) -> List[Any]:
        """
        Generates a positive data set according to the validation parameters.

        :param data_type: Type of data to be validated.
        :return: List[Any]
        """

        values = []

        if self.min is not None:
            values.append(data_type.generate(self.min))
        if self.max is not None:
            values.append(data_type.generate(self.max))

        return values

    def negative(self, data_type: Field) -> List[Any]:
        """
        Generates a negative data set according to the validation parameters.

        :param data_type: Type of data to be validated.
        :return: List[Any]
        """

        if self.min == 0:
            raise ValueError(
                "Неверная длинна коллекции: -1"
            )

        values = []

        if self.min is not None:
            values.append(data_type.generate(self.min - 1))
        if self.max is not None:
            values.append(data_type.generate(self.max + 1))

        return values


class Range(ValidatorABC):
    """Limits the range of number values"""

    def __init__(
            self,
            min: int | float | datetime | date = None,
            max: int | float | datetime | date = None,
            min_inclusive: bool = True,
            max_inclusive: bool = True,
    ):
        """
        Represents a number value range validator

        :param min: Minimum value.
        :param max: Maximum value.
        :param min_inclusive: True if min is within the range of valid number values
        :param max_inclusive: True if max is within the range of valid number values
        """

        if not min and not max:
            raise ValueError("One of the parameters min, max is required")

        if min is not None and max is not None:
            if min >= max:
                raise ValueError("The minimum value cannot be greater than or equal to the maximum")

        self.min = min
        self.min_inclusive = min_inclusive
        self.max = max
        self.max_inclusive = max_inclusive

    def _get_min(self, data_type: Field, positive: bool = True) -> Union[int, float]:
        """
        Returns the minimum acceptable range value for the specified data type.

        :param data_type: Data type.
        :param positive: Positive or negative value.
        :return: Minimum range limit.
        """

        if self.min_inclusive:
            if positive:
                result = self.min
            else:
                result = self.min - data_type.get_step()
        else:
            if positive:
                result = self.min + data_type.get_step()
            else:
                result = self.min

        if isinstance(data_type, Float):
            return float(result)
        return result

    def _get_max(self, data_type: Field, positive: bool) -> Union[int, float]:
        """
        Returns the maximum allowed range value for the specified data type.

        :param data_type: Data type.
        :param positive: Positive or negative value.
        :return: Maximum range limit.
        """

        if self.max_inclusive:
            if positive:
                result = self.max
            else:
                result = self.max + data_type.get_step()
        else:
            if positive:
                result = self.max - data_type.get_step()
            else:
                result = self.max

        if isinstance(data_type, Float):
            return float(result)
        return result

    def positive(self, data_type: Field) -> List[Any]:
        """
        Generates a positive data set according to the validation parameters.

        :param data_type: Type of data to be validated.
        :return: List[Any]
        """

        values = []

        if self.min is not None:
            values.append(self._get_min(data_type, positive=True))
        if self.max is not None:
            values.append(self._get_max(data_type, positive=True))

        return values

    def negative(self, data_type: Field) -> List[Any]:
        """
        Generates a negative data set according to the validation parameters.

        :param data_type: Type of data to be validated.
        :return: List[Any]
        """

        values = []

        if self.min is not None:
            values.append(self._get_min(data_type, positive=False))
        if self.max is not None:
            values.append(self._get_max(data_type, positive=False))

        return values


class Equal(ValidatorABC):
    """Tests for equality"""

    def __init__(self, comparable: Any):
        self.comparable = comparable

    def positive(self, data_type: Field) -> List[Any]:
        return [self.comparable]

    def negative(self, data_type: Field) -> List[Any]:
        return [data_type.get_other_value(value=self.comparable)]


class OneOf(ValidatorABC):
    """Checks for membership in the choices set"""

    def __init__(self, choices: List[Any]):
        self.choices = choices

    def positive(self, data_type: Field) -> List[Any]:
        return self.choices

    def negative(self, data_type: Field) -> List[Any]:
        result = []

        for value in self.choices:
            while True:
                new_value = data_type.get_other_value(value=value)
                # Checking for a random hit in one of the choices values
                if new_value not in self.choices:
                    result += [new_value]
                    break

        return result


class NoneOf(ValidatorABC):
    """Checks for non-membership in the set of choices"""

    def __init__(self, invalid_values: List[Any]):
        self.invalid_values = invalid_values

    def positive(self, data_type: Field) -> List[Any]:
        result = []

        for value in self.invalid_values:
            while True:
                valid_value = data_type.get_other_value(value=value)
                # Checking for a random hit in one of the invalid_values
                if valid_value not in self.invalid_values:
                    result += [valid_value]
                    break

        return result

    def negative(self, data_type: Field) -> List[Any]:
        return self.invalid_values
