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
        self.inner_values = []  # Only for Collections

    def positive(self):
        self.values = ValuesStorage()

        if self.positive_data_from is not None:
            yield from self.positive_data_from()
            return

        for validator in self.validators:
            if isinstance(self, Collection):
                self.inner_values = list(self.data_type.positive())
                values = validator.positive(self)
                for value in values:
                    self._register(value)
            else:
                self._register(validator.positive(self))

        if self.allow_none:
            self._register(None)

        if self.default is not None:
            self._register(self.default)

        if not self.required:
            self._register(Missing())

        if self.positive_data_from is None and not self.validators:
            self.set_positive_values()

        yield from self.values

    def negative(self):
        self.values = ValuesStorage()

        if self.negative_data_from is not None:
            yield from self.negative_data_from()
            return

        for validator in self.validators:
            if isinstance(self, Collection):
                self.inner_values = list(self.data_type.positive())
                values = validator.negative(self)
                for value in values:
                    self._register(value)

                self.inner_values = list(self.data_type.negative())
                values = validator.positive(self)
                for value in values:
                    self._register(value)
            else:
                self._register(validator.negative(self))

        if not self.allow_none:
            self._register(None)

        if self.required:
            self._register(Missing())

        if self.positive_data_from is None:
            self.set_negative_values()

        yield from self.values

    def set_positive_values(self):
        raise NotImplementedError('Implement this method in your data type')

    def set_negative_values(self):
        raise NotImplementedError('Implement this method in your data type')

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
        """Implement this method for the Equal, OneOf и NoneOf validators to work correctly"""

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

    def set_positive_values(self) -> None:
        self._register(self.generate(length=randint(1, 10)))

    def set_negative_values(self) -> None:
        self._register(randint(-100, 100))

    def generate(self, length: int):
        """
        Generates a string of the specified length.

        :param length: String length.
        :return: String.
        """

        return ''.join(choice(ascii_letters) for _ in range(length))

    def get_other_value(self, value: Optional[str]) -> str:
        """Returns an object of type str and not equal to value"""

        if value is None:
            return 'not_comparable'
        return 'not_' + value


class Integer(Field):
    """Integer representation"""

    def __init__(self, step: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step

    def set_positive_values(self) -> None:
        self._register(randint(-100, 100))

    def set_negative_values(self) -> None:
        self._register(
            ''.join(choice(ascii_letters) for _ in range(randint(5, 10)))
        )

    def get_step(self):
        return self.step

    def get_other_value(self, value: Optional[int]) -> int:
        """Returns an object of type int and not equal to value"""

        if value is None:
            return randint(10, 100000)
        return value + randint(10, 100000)


class Float(Field):
    """Floating point representation"""

    def __init__(self, step: float = 0.01, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step

    def set_positive_values(self) -> None:
        self._register(randint(-10000, 10000) / 100)

    def set_negative_values(self) -> None:
        self._register(
            ''.join(choice(ascii_letters) for _ in range(randint(5, 10)))
        )

    def get_step(self):
        return self.step

    def get_other_value(self, value: Optional[float]) -> float:
        """Returns an object of type float and not equal to value"""

        if value is None:
            return randint(1000000, 100000000) / 100
        return value + randint(1000000, 100000000) / 100


class Boolean(Field):
    """Boolean type representation"""

    def set_positive_values(self) -> None:
        self._register([True, False])

    def set_negative_values(self) -> None:
        self._register(
            ''.join(choice(ascii_letters) for _ in range(randint(5, 10)))
        )

    def get_other_value(self, value: Optional[bool]) -> bool:
        """Returns an object of type bool and not equal to value"""

        if value is None:
            return True
        return not value


class DateTime(Field):
    """Datetime type representation"""

    def __init__(self, step: timedelta = timedelta(days=1), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step

    def set_positive_values(self) -> None:
        self._register(datetime.now())

    def set_negative_values(self) -> None:
        self._register('not_datetime')

    def get_step(self) -> timedelta:
        return self.step

    def get_other_value(self, value: Optional[datetime]) -> datetime:
        """Returns an object of type datetime and not equal to value"""

        if value is None:
            return datetime.now()
        return value + timedelta(days=randint(1, 365), minutes=randint(1, 60))


class Date(Field):
    """Date type representation"""

    def __init__(self, step: timedelta = timedelta(days=1), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step

    def set_positive_values(self) -> None:
        self._register(datetime.now().date())

    def set_negative_values(self) -> None:
        self._register('not_date')

    def get_step(self):
        return self.step

    def get_other_value(self, value: date) -> date:
        """Returns an object of type date and not equal to value"""

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

    def set_positive_values(self) -> None:
        self.inner_values = self.data_type.positive()

        for value in self.inner_values:
            self._register([[value for _ in range(randint(1, 5))]])

    def set_negative_values(self) -> None:
        self.inner_values = self.data_type.negative()

        for value in self.inner_values:
            self._register([[value for _ in range(randint(1, 5))]])

    def generate(self, length: int) -> List[Any]:
        return [
            [allowed_value for _ in range(length)]
            for allowed_value in self.inner_values
        ]

    def get_other_value(self, value: list) -> list:
        """Returns an object of type list and not equal to value"""

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

    def set_positive_values(self) -> None:
        self._register(list(self.data_type.positive()))

    def set_negative_values(self) -> None:
        self._register(list(self.data_type.negative()))
