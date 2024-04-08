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
    OneOf,
    NoneOf,
)
from sgen import SGen


def test_nested_simple():
    class Test(SGen):
        name = String()
        age = Integer()
        balance = Float()
        is_admin = Boolean()

    field = Nested(Test())

    datasets_from_sgen = list(field.negative())

    assert len(datasets_from_sgen) == 135


def test_nested_with_validators():
    field_age = Integer(validate=Range(min=18, min_inclusive=False))
    field_balance = Float(allow_none=False, required=True, validate=OneOf(choices=[1, 2, 3, 4, 5]))
    field_is_admin = Boolean(required=True)
    field_keys = Collection(data_type=Integer(), allow_none=False, required=True)
    field_address = String(validate=NoneOf(invalid_values=['Pepega street']))

    class Test(SGen):
        age = field_age
        balance = field_balance
        is_admin = field_is_admin
        keys = field_keys
        address = field_address

    field = Nested(Test())

    datasets_from_sgen = list(field.negative())

    assert len(datasets_from_sgen) == 1863
