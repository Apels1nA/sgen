from tests import has_data_type, Unique
from fields import Float
from utils import Missing
from validate import Range, Equal, OneOf


def test_float():
    field = Float()

    positive_values = field.positive()

    assert len(positive_values) == 3

    assert has_data_type(positive_values, float)
    assert has_data_type(positive_values, type(None))
    assert has_data_type(positive_values, Missing)


def test_allow_none():
    field = Float(allow_none=False)

    assert None not in field.positive()


def test_required():
    field = Float(required=True)

    assert not has_data_type(field.positive(), Missing)


def test_default():
    default = 1.23456789
    field = Float(default=default)

    assert default in field.positive()


def test_positive_data_from():
    def positive_data_generator():
        return 1.0, -9999.9999

    field = Float(positive_data_from=positive_data_generator)

    assert field.positive() == list(positive_data_generator())


# =================================================
# Тесты на взаимодействие типа Float с валидаторами
# =================================================


def test_range():
    min_ = -999.74
    max_ = 998.39

    field = Float(
        validate=Range(
            min=min_, max=max_
        )
    )

    positive_data = field.positive()

    assert min_ in positive_data
    assert max_ in positive_data


def test_range_inclusive():
    min_ = -999.74
    max_ = 998.39

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

    positive_data = field.positive()

    assert min_ + 0.01 in positive_data
    assert max_ - 0.01 in positive_data
    assert None not in positive_data
    assert not has_data_type(positive_data, Missing)


def test_range_default():
    min_ = -999.74
    max_ = 998.39
    default = Unique()

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

    positive_data = field.positive()

    assert min_ + 0.01 in positive_data
    assert max_ - 0.01 in positive_data
    assert None not in positive_data
    assert default in positive_data


def test_equal():
    comparable = Unique()

    field = Float(
        validate=Equal(comparable=comparable)
    )

    field_values = field.positive()

    assert comparable in field_values
    assert None in field_values
    assert has_data_type(field_values, Missing)


def test_equal_allow_none_required():
    comparable = Unique()

    field = Float(
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

    field = Float(
        validate=Equal(comparable=comparable),
        allow_none=False,
        default=default,
    )

    field_values = field.positive()

    assert default in field_values
    assert None not in field_values


def test_one_of():
    choices = [Unique(), Unique(), Unique()]

    field = Float(
        validate=OneOf(choices=choices),
    )

    field_values = field.positive()

    for value in choices:
        assert value in field_values

    assert None in field_values
    assert has_data_type(field_values, Missing)


def test_one_of_allow_none_required():
    choices = [Unique(), Unique(), Unique()]

    field = Float(
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

    field = Float(
        validate=OneOf(choices=choices),
        allow_none=False,
        default=default,
    )

    field_values = field.positive()

    for value in choices:
        assert value in field_values

    assert None not in field_values
    assert default in field_values
