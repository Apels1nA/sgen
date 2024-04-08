from datetime import date

from tests import has_data_type
from sgen.fields import Date
from sgen.utils import Missing
from sgen.validate import Range, Equal, OneOf


def test_date():
    field = Date()

    positive_values = list(field.positive())

    assert len(positive_values) == 3

    assert has_data_type(positive_values, date)
    assert has_data_type(positive_values, type(None))
    assert has_data_type(positive_values, Missing)


def test_allow_none():
    field = Date(allow_none=False)

    assert None not in list(field.positive())


def test_required():
    field = Date(required=True)

    assert not has_data_type(list(field.positive()), Missing)


def test_default():
    default = 1.23456789
    field = Date(default=default)

    assert default in list(field.positive())


def test_positive_data_from():
    def positive_data_generator():
        return 1.0, -9999.9999

    field = Date(positive_data_from=positive_data_generator)

    assert list(field.positive()) == list(positive_data_generator())


# =================================================
# Тесты на взаимодействие типа Date с валидаторами
# =================================================


def test_range():
    min_ = -999.74
    max_ = 998.39

    field = Date(
        validate=Range(
            min=min_, max=max_
        )
    )

    positive_data = list(field.positive())

    assert min_ in positive_data
    assert max_ in positive_data


def test_range_inclusive():
    min_ = date(2022, 1, 1)
    max_ = date(2023, 1, 1)

    field = Date(
        validate=Range(
            min=min_,
            max=max_,
            min_inclusive=False,
            max_inclusive=False,
        ),
        allow_none=False,
        required=True,
    )

    positive_data = list(field.positive())

    assert min_ + field.get_step() in positive_data
    assert max_ - field.get_step() in positive_data
    assert None not in positive_data
    assert not has_data_type(positive_data, Missing)


def test_range_default():
    min_ = date(2022, 1, 1)
    max_ = date(2023, 1, 1)
    default = date(1996, 12, 3)

    field = Date(
        validate=Range(
            min=min_,
            max=max_,
            min_inclusive=False,
            max_inclusive=False,
        ),
        allow_none=False,
        default=default,
    )

    positive_data = list(field.positive())

    assert min_ + field.get_step() in positive_data
    assert max_ - field.get_step() in positive_data
    assert None not in positive_data
    assert default in positive_data


def test_equal():
    comparable = date(1996, 12, 3)

    field = Date(
        validate=Equal(comparable=comparable)
    )

    field_values = list(field.positive())

    assert comparable in field_values
    assert None in field_values
    assert has_data_type(field_values, Missing)


def test_equal_allow_none_required():
    comparable = date(1996, 12, 3)

    field = Date(
        validate=Equal(comparable=comparable),
        allow_none=False,
        required=True,
    )

    field_values = list(field.positive())

    assert comparable in field_values
    assert None not in field_values
    assert not has_data_type(field_values, Missing)


def test_equal_default():
    comparable = date(1996, 12, 3)
    default = date(2000, 12, 3)

    field = Date(
        validate=Equal(comparable=comparable),
        allow_none=False,
        default=default,
    )

    field_values = list(field.positive())

    assert default in field_values
    assert None not in field_values


def test_one_of():
    choices = [
        date(1996, 12, 3),
        date(2000, 12, 3),
        date(2002, 12, 3)
    ]

    field = Date(
        validate=OneOf(choices=choices),
    )

    field_values = list(field.positive())

    for value in choices:
        assert value in field_values

    assert None in field_values
    assert has_data_type(field_values, Missing)


def test_one_of_allow_none_required():
    choices = [
        date(1996, 12, 3),
        date(2000, 12, 3),
        date(2002, 12, 3)
    ]

    field = Date(
        validate=OneOf(choices=choices),
        allow_none=False,
        required=True,
    )

    field_values = list(field.positive())

    for value in choices:
        assert value in field_values

    assert None not in field_values
    assert not has_data_type(field_values, Missing)


def test_one_of_default():
    choices = [
        date(1996, 12, 3),
        date(2000, 12, 3),
        date(2002, 12, 3)
    ]
    default = date(1991, 12, 3)

    field = Date(
        validate=OneOf(choices=choices),
        allow_none=False,
        default=default,
    )

    field_values = list(field.positive())

    for value in choices:
        assert value in field_values

    assert None not in field_values
    assert default in field_values
