from tests import has_data_type, Unique
from sgen.fields import String
from sgen.utils import Missing
from sgen.validate import Length, Equal, OneOf


def test_string():
    field = String()

    negative_values = list(field.negative())

    assert len(negative_values) == 1
    assert isinstance(negative_values[0], int)


def test_not_allow_none():
    field = String(allow_none=False)

    assert None in list(field.negative())


def test_required():
    field = String(required=True)

    assert has_data_type(list(field.negative()), Missing)


def test_negative_data_from():
    def negative_data_from():
        return 'a', 666, None, Missing

    field = String(negative_data_from=negative_data_from)

    assert list(field.negative()) == list(negative_data_from())


# ==================================================
# Тесты на взаимодействие типа String с валидаторами
# ==================================================


def test_length():
    min_ = 999
    max_ = 1111

    field = String(validate=Length(min=min_, max=max_))

    for value in list(field.negative()):
        if isinstance(value, str):
            assert len(value) in [min_ - 1, max_ + 1]


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

    field_values = list(field.negative())

    for value in field_values:
        if isinstance(value, str):
            assert len(value) in [min_, max_]

    assert None in field_values
    assert has_data_type(field_values, Missing)


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

    field_values = list(field.negative())

    for value in field_values:
        if isinstance(value, str):
            assert len(value) in [min_, max_]

    assert None in field_values
    assert default not in field_values


def test_equal():
    comparable = 'str_text'

    field = String(
        validate=Equal(comparable=comparable)
    )

    field_values = list(field.negative())

    assert comparable not in field_values
    assert None not in field_values
    assert has_data_type(field_values, int)


def test_equal_allow_none_required():
    comparable = 'str_text'

    field = String(
        validate=Equal(comparable=comparable),
        allow_none=False,
        required=True,
    )

    field_values = list(field.negative())

    assert comparable not in field_values
    assert None in field_values
    assert has_data_type(field_values, int)
    assert has_data_type(field_values, type(None))
    assert has_data_type(field_values, Missing)


def test_equal_default():
    comparable = 'str_text'
    default = 'str_text_def'

    field = String(
        validate=Equal(comparable=comparable),
        allow_none=False,
        default=default,
    )

    field_values = list(field.negative())

    assert default not in field_values
    assert None in field_values


def test_one_of():
    choices = ['a_1', 'a_2', 'a_3']

    field = String(
        validate=OneOf(choices=choices),
    )

    field_values = list(field.negative())

    for value in choices:
        assert value not in field_values

    assert None not in field_values
    assert has_data_type(field_values, int)
    assert not has_data_type(field_values, Missing)


def test_one_of_allow_none_required():
    choices = ['a_1', 'a_2', 'a_3']

    field = String(
        validate=OneOf(choices=choices),
        allow_none=False,
        required=True,
    )

    field_values = list(field.negative())

    for value in choices:
        assert value not in field_values

    assert None in field_values
    assert has_data_type(field_values, int)
    assert has_data_type(field_values, Missing)


def test_one_of_default():
    choices = ['a_1', 'a_2', 'a_3']
    default = 'str_text_def'

    field = String(
        validate=OneOf(choices=choices),
        allow_none=False,
        default=default,
    )

    field_values = list(field.negative())

    for value in choices:
        assert value not in field_values

    assert None in field_values
    assert has_data_type(field_values, int)
    assert default not in field_values
