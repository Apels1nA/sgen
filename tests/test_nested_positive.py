from itertools import product

from sgen.fields import (
    Nested,
    String,
    Integer,
    Float,
    Boolean,
    Collection
)
from sgen.validate import (
    Range,
    Length,
    OneOf,
    NoneOf,
    Equal,
)
from sgen import SGen


def test_nested_simple():
    class Test(SGen):
        name = String()
        age = Integer()
        balance = Float()
        is_admin = Boolean()

    field = Nested(Test())

    datasets_from_sgen = list(field.positive())
    datasets_from_system_library = list(product(
        String().positive(),
        Integer().positive(),
        Float().positive(),
        Boolean().positive(),
    ))

    assert len(datasets_from_sgen) == len(datasets_from_system_library) + 2  # 2 = none + missing


def test_nested_with_validators():
    field_name = String(allow_none=False, default='Aboba', validate=Length(min=10, max=40))
    field_age = Integer(validate=Range(min=18, min_inclusive=False))
    field_balance = Float(allow_none=False, required=True, validate=OneOf(choices=[1, 2, 3, 4, 5]))
    field_is_admin = Boolean(required=True)
    field_keys = Collection(data_type=Integer(), allow_none=False, required=True)
    field_address = String(validate=NoneOf(invalid_values=['Pepega street']))
    field_car = String(validate=Equal(comparable='Jaguar XF'))

    class Test(SGen):
        name = field_name
        age = field_age
        balance = field_balance
        is_admin = field_is_admin
        keys = field_keys
        address = field_address
        car = field_car

    field = Nested(Test())

    datasets_from_sgen = list(field.positive())
    datasets_from_system_library = list(product(
        field_name.positive(),
        field_age.positive(),
        field_balance.positive(),
        field_is_admin.positive(),
        field_keys.positive(),
        field_address.positive(),
        field_car.positive(),
    ))

    assert len(datasets_from_sgen) == len(datasets_from_system_library) + 2  # 2 = none + missing
