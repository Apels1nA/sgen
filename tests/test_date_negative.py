from datetime import datetime, date

from tests import has_data_type
from sgen.fields import Date
from sgen.utils import Missing
from sgen.validate import Range, Equal, OneOf


def test_date():
    field = Date()

    negative_values = list(field.negative())

    assert len(negative_values) == 1
    assert not isinstance(negative_values[0], date)


def test_allow_none():
    field = Date(allow_none=False)

    assert None in list(field.negative())


def test_required():
    field = Date(required=True)

    # src.sgen.utils.Missing
    # sgen.utils.Missing

    assert has_data_type(list(field.negative()), Missing)


def test_negative_data_from():
    def negative_data_from():
        return None, Missing

    field = Date(negative_data_from=negative_data_from)

    assert list(field.negative()) == list(negative_data_from())


# =================================================
# Тесты на взаимодействие типа Float с валидаторами
# =================================================


def test_range():
    min_ = date(2022, 1, 1)
    max_ = date(2023, 1, 1)

    field = Date(
        validate=Range(
            min=min_, max=max_
        )
    )

    negative_data = list(field.negative())

    assert min_ - field.get_step() in negative_data
    assert max_ + field.get_step() in negative_data


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

    negative_data = list(field.negative())

    assert min_ in negative_data
    assert max_ in negative_data
    assert None in negative_data
    assert has_data_type(negative_data, Missing)


def test_range_default():
    min_ = datetime(2022, 1, 1)
    max_ = datetime(2023, 1, 1)
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

    negative_data = list(field.negative())

    assert min_ in negative_data
    assert max_ in negative_data
    assert None in negative_data
    assert default not in negative_data


def test_equal():
    comparable = date(1996, 12, 3)

    field = Date(
        validate=Equal(comparable=comparable)
    )

    field_values = list(field.negative())

    assert comparable not in field_values
    assert None not in field_values
    assert has_data_type(field_values, str)


def test_equal_allow_none_required():
    comparable = date(1996, 12, 3)

    field = Date(
        validate=Equal(comparable=comparable),
        allow_none=False,
        required=True,
    )

    field_values = list(field.negative())

    assert comparable not in field_values
    assert None in field_values
    assert has_data_type(field_values, str)
    assert has_data_type(field_values, Missing)


def test_equal_default():
    comparable = date(1996, 12, 3)
    default = date(2000, 12, 3)

    field = Date(
        validate=Equal(comparable=comparable),
        allow_none=False,
        default=default,
    )

    field_values = list(field.negative())

    assert None in field_values
    assert default not in field_values


def test_one_of():
    choices = [
        date(1996, 12, 3),
        date(2000, 12, 3),
        date(2002, 12, 3)
    ]

    field = Date(
        validate=OneOf(choices=choices),
    )

    field_values = list(field.negative())

    for value in choices:
        assert value not in field_values

    assert None not in field_values
    assert has_data_type(field_values, str)
    assert not has_data_type(field_values, Missing)


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

    field_values = list(field.negative())

    for value in choices:
        assert value not in field_values

    assert None in field_values
    assert has_data_type(field_values, str)
    assert has_data_type(field_values, Missing)


def test_one_of_default():
    choices = [
        date(1996, 12, 3),
        date(2000, 12, 3),
        date(2002, 12, 3)
    ]
    default = date(1992, 12, 3)

    field = Date(
        validate=OneOf(choices=choices),
        allow_none=False,
        default=default,
    )

    field_values = list(field.negative())

    for value in choices:
        assert value not in field_values

    assert has_data_type(field_values, str)
    assert None in field_values
    assert default not in field_values
