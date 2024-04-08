from tests import has_data_type
from sgen.fields import Integer
from sgen.validate import Range, Equal, OneOf
from sgen.utils import Missing


def test_int():
    field = Integer()

    negative_values = list(field.negative())

    assert len(negative_values) == 1
    assert not isinstance(negative_values[0], int)


def test_allow_none():
    field = Integer(allow_none=False)

    assert None in list(field.negative())


def test_required():
    field = Integer(required=True)

    assert has_data_type(list(field.negative()), Missing)


def test_negative_data_from():
    def negative_data_from():
        return 'a', 666, None, Missing

    field = Integer(negative_data_from=negative_data_from)

    assert list(field.negative()) == list(negative_data_from())


# ===================================================
# Тесты на взаимодействие типа Integer с валидаторами
# ===================================================


def test_range():
    min_ = -998
    max_ = 649

    field = Integer(
        validate=Range(
            min=min_, max=max_
        )
    )

    negative_data = list(field.negative())

    assert min_ - 1 in negative_data
    assert max_ + 1 in negative_data


def test_range_inclusive():
    min_ = -998
    max_ = 649

    field = Integer(
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
    min_ = -998
    max_ = 649
    default = 619234

    field = Integer(
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
    comparable = 619234

    field = Integer(
        validate=Equal(comparable=comparable)
    )

    field_values = list(field.negative())

    assert comparable not in field_values
    assert None not in field_values
    assert has_data_type(field_values, str)


def test_equal_allow_none_required():
    comparable = 619234

    field = Integer(
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
    comparable = 619234
    default = 8357

    field = Integer(
        validate=Equal(comparable=comparable),
        allow_none=False,
        default=default,
    )

    field_values = list(field.negative())

    assert default not in field_values
    assert None in field_values


def test_one_of():
    choices = [1111, 2222, 3333]

    field = Integer(
        validate=OneOf(choices=choices),
    )

    field_values = list(field.negative())

    for value in choices:
        assert value not in field_values

    assert None not in field_values
    assert has_data_type(field_values, str)
    assert not has_data_type(field_values, Missing)


def test_one_of_allow_none_required():
    choices = [1111, 2222, 3333]

    field = Integer(
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
    choices = [1111, 2222, 3333]
    default = 619234

    field = Integer(
        validate=OneOf(choices=choices),
        allow_none=False,
        default=default,
    )

    field_values = list(field.negative())

    for value in choices:
        assert value not in field_values

    assert None in field_values
    assert has_data_type(field_values, str)
    assert default not in field_values
