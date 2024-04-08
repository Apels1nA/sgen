from tests import has_data_type, Unique
from sgen.fields import Boolean
from sgen.utils import Missing
from sgen.validate import Equal, OneOf


def test_boolean():
    field = Boolean()

    positive_values = list(field.positive())

    assert len(positive_values) == 4

    has_true = False
    has_false = False
    for value in positive_values:
        if isinstance(value, bool) and value:
            has_true = True
        if isinstance(value, bool) and not value:
            has_false = True

    assert has_true
    assert has_false
    assert has_data_type(positive_values, type(None))
    assert has_data_type(positive_values, Missing)


def test_allow_none():
    field = Boolean(allow_none=False)

    assert None not in list(field.positive())


def test_required():
    fields = Boolean(required=True)

    assert not has_data_type(list(fields.positive()), Missing)


def test_default():
    field = Boolean(default=False)

    assert False in list(field.positive())


def test_positive_data_from():
    def positive_data_generator():
        return 0, 1, False, True

    field = Boolean(positive_data_from=positive_data_generator)

    assert list(field.positive()) == list(positive_data_generator())


# ===================================================
# Тесты на взаимодействие типа Boolean с валидаторами
# ===================================================


def test_equal():
    comparable = Unique()

    field = Boolean(
        validate=Equal(comparable=comparable)
    )

    field_values = list(field.positive())

    assert comparable in field_values
    assert None in field_values
    assert has_data_type(field_values, Missing)


def test_equal_allow_none_required():
    comparable = Unique()

    field = Boolean(
        validate=Equal(comparable=comparable),
        allow_none=False,
        required=True,
    )

    field_values = list(field.positive())

    assert comparable in field_values
    assert None not in field_values
    assert not has_data_type(field_values, Missing)


def test_equal_default():
    comparable = Unique()
    default = Unique()

    field = Boolean(
        validate=Equal(comparable=comparable),
        allow_none=False,
        default=default,
    )

    field_values = list(field.positive())

    assert default in field_values
    assert None not in field_values


def test_one_of():
    choices = [Unique(), Unique(), Unique()]

    field = Boolean(
        validate=OneOf(choices=choices),
    )

    field_values = list(field.positive())

    for value in choices:
        assert value in field_values

    assert None in field_values
    assert has_data_type(field_values, Missing)


def test_one_of_allow_none_required():
    choices = [Unique(), Unique(), Unique()]

    field = Boolean(
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
    choices = [Unique(), Unique(), Unique()]
    default = Unique()

    field = Boolean(
        validate=OneOf(choices=choices),
        allow_none=False,
        default=default,
    )

    field_values = list(field.positive())

    assert default in field_values
    assert None not in field_values
