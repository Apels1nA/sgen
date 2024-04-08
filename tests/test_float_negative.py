from tests import has_data_type
from sgen.fields import Float
from sgen.utils import Missing
from sgen.validate import Range, Equal, OneOf


def test_float():
    field = Float()

    negative_values = list(field.negative())

    assert len(negative_values) == 1
    assert not isinstance(negative_values[0], float)


def test_allow_none():
    field = Float(allow_none=False)

    assert None in list(field.negative())


def test_required():
    field = Float(required=True)

    assert has_data_type(list(field.negative()), Missing)


def test_negative_data_from():
    def negative_data_from():
        return 'a', 333.44, None, Missing

    field = Float(negative_data_from=negative_data_from)

    assert list(field.negative()) == list(negative_data_from())


# =================================================
# Тесты на взаимодействие типа Float с валидаторами
# =================================================


def test_range():
    min_ = -673.94
    max_ = 98.01

    field = Float(
        validate=Range(
            min=min_, max=max_
        )
    )

    negative_data = list(field.negative())

    assert min_ - 0.01 in negative_data
    assert max_ + 0.01 in negative_data


def test_range_inclusive():
    min_ = -673.94
    max_ = 98.01

    field = Float(
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
    min_ = -673.94
    max_ = 98.01
    default = 55.19

    field = Float(
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
    comparable = 55.19

    field = Float(
        validate=Equal(comparable=comparable)
    )

    field_values = list(field.negative())

    assert comparable not in field_values
    assert None not in field_values
    assert has_data_type(field_values, str)


def test_equal_allow_none_required():
    comparable = 55.19

    field = Float(
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
    comparable = 55.19
    default = -87.009

    field = Float(
        validate=Equal(comparable=comparable),
        allow_none=False,
        default=default,
    )

    field_values = list(field.negative())

    assert None in field_values
    assert default not in field_values


def test_one_of():
    choices = [1.1, 2.2, 3.3]

    field = Float(
        validate=OneOf(choices=choices),
    )

    field_values = list(field.negative())

    for value in choices:
        assert value not in field_values

    assert None not in field_values
    assert has_data_type(field_values, str)
    assert not has_data_type(field_values, Missing)


def test_one_of_allow_none_required():
    choices = [1.1, 2.2, 3.3]

    field = Float(
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
    choices = [1.1, 2.2, 3.3]
    default = 55.087

    field = Float(
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
