from uuid import uuid4

from tests import has_data_type, Unique
from fields import String
from utils import Missing
from validate import Length, Equal, OneOf


def test_string():
    field = String()

    positive_values = field.positive()

    assert len(positive_values) == 3

    assert has_data_type(positive_values, str)
    assert has_data_type(positive_values, type(None))
    assert has_data_type(positive_values, Missing)


def test_not_allow_none():
    field = String(allow_none=False)

    positive_values = field.positive()

    assert None not in positive_values


def test_default():
    default = uuid4().hex
    field = String(default=default)

    assert default in field.positive()


def test_required():
    field = String(required=True)

    assert not has_data_type(field.positive(), Missing)


def test_positive_data_from():
    def positive_data_generator():
        return 'a', '1', None, Missing

    field = String(positive_data_from=positive_data_generator)

    assert field.positive() == list(positive_data_generator())


# ==================================================
# Тесты на взаимодействие типа String с валидаторами
# ==================================================


def test_length():
    min_ = 999
    max_ = 1111

    field = String(validate=Length(min=min_, max=max_))

    for value in field.positive():
        if isinstance(value, str):
            assert len(value) in [min_, max_]


def test_length_allow_none_required():
    min_ = 999
    max_ = 1111

    field = String(
        validate=Length(
            min=min_,
            max=max_,
            min_inclusive=False,
            max_inclusive=False,
        ),
        allow_none=False,
        required=True,
    )

    field_values = field.positive()

    for value in field_values:
        if isinstance(value, str):
            assert len(value) in [min_ + 1, max_ - 1]

    assert None not in field_values
    assert not has_data_type(field_values, Missing)


def test_length_default():
    min_ = 999
    max_ = 1111
    default = Unique()

    field = String(
        validate=Length(
            min=min_,
            max=max_,
            min_inclusive=False,
            max_inclusive=False,
        ),
        allow_none=False,
        default=default,
    )

    field_values = field.positive()

    for value in field_values:
        if isinstance(value, str):
            assert len(value) in [min_ + 1, max_ - 1]

    assert None not in field_values
    assert default in field_values


def test_equal():
    comparable = Unique()

    field = String(
        validate=Equal(comparable=comparable)
    )

    field_values = field.positive()

    assert comparable in field_values
    assert None in field_values
    assert has_data_type(field_values, Missing)


def test_equal_allow_none_required():
    comparable = Unique()

    field = String(
        validate=Equal(comparable=comparable),
        allow_none=False,
        required=True,
    )

    field_values = field.positive()

    assert comparable in field_values
    assert None not in field_values
    assert not has_data_type(field_values, Missing)


def test_equal_default():
    comparable = Unique()
    default = Unique()

    field = String(
        validate=Equal(comparable=comparable),
        allow_none=False,
        default=default,
    )

    field_values = field.positive()

    assert default in field_values
    assert None not in field_values


def test_one_of():
    choices = [Unique(), Unique(), Unique()]

    field = String(
        validate=OneOf(choices=choices),
    )

    field_values = field.positive()

    for value in choices:
        assert value in field_values

    assert None in field_values
    assert has_data_type(field_values, Missing)


def test_one_of_allow_none_required():
    choices = [Unique(), Unique(), Unique()]

    field = String(
        validate=OneOf(choices=choices),
        allow_none=False,
        required=True,
    )

    field_values = field.positive()

    for value in choices:
        assert value in field_values

    assert None not in field_values
    assert not has_data_type(field_values, Missing)


def test_one_of_default():
    choices = [Unique(), Unique(), Unique()]
    default = Unique()

    field = String(
        validate=OneOf(choices=choices),
        allow_none=False,
        default=default,
    )

    field_values = field.positive()

    for value in choices:
        assert value in field_values

    assert None not in field_values
    assert default in field_values
