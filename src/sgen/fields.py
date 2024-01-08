from typing import Iterable, Callable, Any, List, Union, Optional
from string import ascii_letters
from random import choice, randint
from datetime import datetime, date, timedelta

from sgen.base import FieldABC, ValidatorABC
from sgen.utils import is_iterable_but_not_string, Missing, ValuesStorage


__all__ = [
    "Field",
    "String",
    "Integer",
    "Float",
    "Boolean",
    "DateTime",
    "Date",
    "Collection",
    "Nested",
]


class Field(FieldABC):
    """Base class for data types"""

    def __init__(
        self,
        validate: (
            ValidatorABC
            | Iterable[ValidatorABC]
            | None
        ) = None,
        positive_data_from: Callable[[], Iterable] = None,
        negative_data_from: Callable[[], Iterable] = None,
        allow_none: bool = True,
        required: bool = False,
        default: Any = None,
    ):
        if validate is None:
            self.validators = []
        elif callable(validate) or isinstance(validate, ValidatorABC):
            self.validators = [validate]
        elif is_iterable_but_not_string(validate):
            raise NotImplemented("Currently several validators are not supported")

        if (positive_data_from or negative_data_from) and default:
            raise ValueError("The data_from and default parameters cannot be passed simultaneously")
        if required and default:
            raise ValueError("The required and default parameters cannot be passed simultaneously")

        self.positive_data_from = positive_data_from
        self.negative_data_from = negative_data_from
        self.default = default
        self.allow_none = allow_none
        self.required = required
        self.values = ValuesStorage()

    def positive(self):
        self.values = ValuesStorage()
        if self.positive_data_from is not None:
            self._register(list(self.positive_data_from()))
            return

        for validator in self.validators:
            if not isinstance(self, Collection):
                self._register(validator.positive(self))

        if self.allow_none:
            self._register(None)

        if self.default is not None:
            self._register(self.default)

        if not self.required:
            self._register(Missing())

    def negative(self):
        self.values = ValuesStorage()
        if self.negative_data_from is not None:
            self._register(list(self.negative_data_from()))
            return

        for validator in self.validators:
            if not isinstance(self, Collection):
                self._register(validator.negative(self))

        if not self.allow_none:
            self._register(None)

        if self.required:
            self._register(Missing())

    def generate(self, length):
        """Implement this method for the Length validator to work correctly"""

        raise NotImplemented(
            "To allow the Length validator to work with iterable data types"
            "you need to implement the generate method, which will return a collection of length length"
        )

    def get_step(self):
        """Implement this method for the Range validator to work correctly"""

        raise NotImplemented(
            "To allow the Range validator to work with numeric data types"
            "you need to implement a get_step method that will return the step for a numeric data type"
        )

    def get_other_value(self, value: Any):
        """Реализуйте этот метод для корректной работы валидаторов Equal, OneOf и NoneOf"""

        raise NotImplemented(
            "For the Equal, OneOf and NoneOf validators to work, you need"
            "implement the get_other_value method, which will return a value not equal to value"
        )

    def _register(self, for_register: Union[Any, List[Any]]):
        """Adds a new value/values to the field's list of values if it is not already present"""

        if isinstance(for_register, list):
            for value in for_register:
                if value not in self.values:
                    self.values.append(value)
        else:
            if for_register not in self.values:
                self.values.append(for_register)


class String(Field):
    """String representation"""

    def positive(self) -> List[Union[None, Missing, str]]:
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        if not self.validators:
            self._register(self.generate(length=randint(1, 10)))

        return self.values

    def negative(self) -> List[Union[None, Missing, str, int]]:
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self._register(randint(-100, 100))

        return self.values

    def generate(self, length: int):
        """
        Generates a string of the specified length.

        :param length: String length.
        :return: String.
        """

        return ''.join(choice(ascii_letters) for _ in range(length))

    def get_other_value(self, value: Optional[str]) -> str:
        if value is None:
            return 'not_comparable'
        return 'not_' + value


class Integer(Field):
    """Integer representation"""

    def __init__(self, step: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step

    def positive(self) -> List[Union[None, Missing, int]]:
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        if not self.validators:
            self._register(randint(-100, 100))

        return self.values

    def negative(self) -> List[Union[None, Missing, int, str]]:
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self._register(
            ''.join(choice(ascii_letters) for _ in range(randint(5, 10)))
        )

        return self.values

    def get_step(self):
        return self.step

    def get_other_value(self, value: Optional[int]) -> int:
        if value is None:
            return randint(10, 100000)
        return value + randint(10, 100000)


class Float(Field):
    """Floating point representation"""

    def __init__(self, step: float = 0.01, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step

    def positive(self) -> List[Union[None, Missing, float]]:
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        if not self.validators:
            self._register(randint(-10000, 10000) / 100)

        return self.values

    def negative(self) -> List[Union[None, Missing, float, str]]:
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self._register(
            ''.join(choice(ascii_letters) for _ in range(randint(5, 10)))
        )

        return self.values

    def get_step(self):
        return self.step

    def get_other_value(self, value: Optional[float]) -> float:
        if value is None:
            return randint(1000000, 100000000) / 100
        return value + randint(1000000, 100000000) / 100


class Boolean(Field):
    """Boolean type representation"""

    def positive(self) -> List[Union[None, Missing, bool]]:
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        if not self.validators:
            self._register([True, False])

        return self.values

    def negative(self) -> List[Union[None, Missing, bool, str]]:
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self._register(
            ''.join(choice(ascii_letters) for _ in range(randint(5, 10)))
        )

        return self.values

    def get_other_value(self, value: Optional[bool]) -> bool:
        if value is None:
            return True
        return not value


class DateTime(Field):
    """Datetime type representation"""

    def __init__(self, step: timedelta = timedelta(days=1), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step

    def positive(self) -> List[Union[None, Missing, datetime]]:
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        if not self.validators:
            self._register(datetime.now())

        return self.values

    def negative(self) -> List[Union[None, Missing, datetime, str]]:
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self._register('not_datetime')

        return self.values

    def get_step(self) -> timedelta:
        return self.step

    def get_other_value(self, value: Optional[datetime]) -> datetime:
        if value is None:
            return datetime.now()
        return value + timedelta(days=randint(1, 365), minutes=randint(1, 60))


class Date(Field):
    """Date type representation"""

    def __init__(self, step: timedelta = timedelta(days=1), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step

    def positive(self) -> List[Union[None, Missing, date]]:
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        if not self.validators:
            self._register(datetime.now().date())

        return self.values

    def negative(self) -> List[Union[None, Missing, date, str]]:
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self._register('not_date')

        return self.values

    def get_step(self):
        return self.step

    def get_other_value(self, value: date) -> date:
        if value is None:
            return datetime.now().date()
        return value + timedelta(days=randint(1, 365))


class Collection(Field):
    """List view"""

    def __init__(self, data_type: Union[FieldABC, 'SGen'], *args, **kwargs):
        """
        Initializes the collection by adding a new data_type parameter to it

        :param data_type: Collection data type
        """

        super().__init__(*args, **kwargs)
        self.data_type = data_type
        self.inner_values = []

    def _register(self, for_register: Union[Any, List[Any]]):
        """
        Adds a new value/values to the field's list of values if it is not already present
        Additionally, it clears lists of the Missing value, since doing this at the SGen class level is inconvenient

        :param for_register: Adds a value or list of logged values
        """

        if isinstance(for_register, list):
            self.values.extend([
                list(filter(lambda item: not isinstance(item, Missing), value))  # Filtering Missing within lists
                for value in for_register
                if list(filter(lambda item: not isinstance(item, Missing), value)) or not self.validators
            ])
        else:
            if for_register not in self.values:
                self.values.append(for_register)

    def positive(self) -> List[Any]:
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        self.inner_values = self.data_type.positive()

        for validator in self.validators:
            values = validator.positive(self)
            for value in values:
                self._register(value)

        if not self.validators:
            for value in self.inner_values:
                self._register([[value for _ in range(randint(1, 5))]])
        return self.values

    def negative(self) -> List[Any]:
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        self.inner_values = self.data_type.positive()
        for validator in self.validators:
            values = validator.negative(self)
            for value in values:
                self._register(value)

        self.inner_values = self.data_type.negative()
        for validator in self.validators:
            values = validator.positive(self)
            for value in values:
                self._register(value)

        if not self.validators:
            for value in self.inner_values:
                self._register([[value for _ in range(randint(1, 5))]])

        return self.values

    def generate(self, length: int) -> List[Any]:
        return [
            [allowed_value for _ in range(length)]
            for allowed_value in self.inner_values
        ]

    def get_other_value(self, value: list) -> list:
        if value is None:
            return [self.data_type.get_other_value(value=value)]
        return value * 2


class Nested(Field):
    """Entity View"""

    def __init__(self, data_type: 'SGen', *args, **kwargs):
        """
        Initializes a nested schema by adding a new data_type parameter to it

        :param data_type: Schema data type
        """

        super().__init__(*args, **kwargs)
        self.data_type = data_type

    def positive(self):
        super().positive()

        if self.positive_data_from is not None:
            return self.values

        for structure in self.data_type.positive():
            yield structure

    def negative(self):
        super().negative()

        if self.negative_data_from is not None:
            return self.values

        for structure in self.data_type.negative():
            yield structure
