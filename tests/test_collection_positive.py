from sgen.fields import (
    Collection,
    String,
    Float,
    Boolean,
    Integer,
)
from sgen.validate import Length
from tests import Unique, has_data_type
from sgen.utils import Missing

DATA_TYPES = [
    [String, str],
    [Integer, int],
    [Float, float],
    [Boolean, bool],
]


def test_simple():
    for type_ in DATA_TYPES:
        field = Collection(data_type=type_[0]())

        field_values = list(field.positive())

        assert None in field_values
        assert has_data_type(field_values, Missing)
        assert has_data_type(field_values, list)

        for value in field_values:
            if isinstance(value, list):
                assert (
                    has_data_type(value, type_[1]) or
                    not value or
                    None in value
                )

        default = Unique()
        field = Collection(data_type=type_[0](), default=default)
        assert default in list(field.positive())


def test_length_validator():
    min_ = 100
    max_ = 200

    for type_ in DATA_TYPES:
        field = Collection(
            data_type=type_[0](allow_none=False, required=True),
            validate=Length(
                min=min_,
                max=max_,
            ),
            allow_none=False,
            required=True,
        )

        field_values = list(field.positive())

        assert None not in field_values
        assert not has_data_type(field_values, Missing)
        assert has_data_type(field_values, list)

        for value in field_values:
            if isinstance(value, list):
                assert len(value) in [min_, max_]
