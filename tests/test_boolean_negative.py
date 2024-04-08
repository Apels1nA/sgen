from tests import has_data_type, Unique
from sgen.fields import Boolean
from sgen.utils import Missing
from sgen.validate import Equal, OneOf


def test_boolean():
    field = Boolean()

    negative_values = list(field.negative())

    assert len(negative_values) == 1
    assert not isinstance(negative_values[0], bool)


def test_allow_none():
    field = Boolean(allow_none=False)

    assert None in list(field.negative())


def test_required():
    field = Boolean(required=True)

    negative_values = list(field.negative())

    assert has_data_type(negative_values, Missing)


def test_negative_data_from():
    def negative_data_from():
        return 'a', -88.17, None

    field = Boolean(negative_data_from=negative_data_from)

    assert list(field.negative()) == list(negative_data_from())


# ===================================================
# Тесты на взаимодействие типа Boolean с валидаторами
# ===================================================


def test_equal():
    comparable = Unique()

    field = Boolean(
        validate=Equal(comparable=comparable)
    )

    field_values = list(field.negative())

    assert comparable not in field_values
    assert None not in field_values
    assert has_data_type(field_values, str)


def test_equal_allow_none_and_required():
    comparable = Unique()

    field = Boolean(
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
    comparable = Unique()
    default = Unique()

    field = Boolean(
        validate=Equal(comparable=comparable),
        allow_none=False,
        default=default,
    )

    field_values = list(field.negative())

    assert default not in field_values
    assert None in field_values


def test_one_of():
    choices = [Unique(), Unique(), Unique()]

    field = Boolean(
        validate=OneOf(choices=choices),
    )

    field_values = list(field.negative())

    for value in choices:
        assert value not in field_values

    assert None not in field_values
    assert has_data_type(field_values, str)
    assert not has_data_type(field_values, Missing)


def test_one_of_allow_none_required():
    choices = [Unique(), Unique(), Unique()]

    field = Boolean(
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
    choices = [Unique(), Unique(), Unique()]
    default = Unique()

    field = Boolean(
        validate=OneOf(choices=choices),
        allow_none=False,
        default=default,
    )

    field_values = list(field.negative())

    assert default not in field_values
    assert None in field_values
