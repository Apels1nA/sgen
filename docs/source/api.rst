.. _api:

API Documentation
=================

This document specifies SGen's APIs.

Schema
------

.. py:class:: SGen

    .. py:method:: fields(is_positive: bool) -> List[SchemaField]

        Returns a list of positive field generators if ``is_positive=True``

        :param bool is_positive: ``True`` if positive data generators need to be returned
        :return: List of objects of type ``SchemaField``

    .. py:method:: positive() -> Generator:

        :return: List of valid dictionaries
        :rtype: Generator object

    .. py:method:: negative() -> Generator:

        :return: List of not valid dictionaries
        :rtype: Generator object

    Class :py:class:`SGen` can be used to:

    * Description of the data structure
    * Generating valid data sets
    * Generating not valid data sets

    Example:

    .. code-block:: python

        from sgen import Sgen, fields


        class User(SGen):
            name = fields.String(required=True)
            age = fields.Integer(allow_none=False)

        user_sgen = User()
        user_sgen.positive()  # Will return a set of valid data
        user_sgen.negative()  # Will return a set of not valid data

Fields
------

.. py:class:: Field()

    .. py:method:: __init__(validate: (ValidatorABC | Iterable[ValidatorABC] | None) = None, positive_data_from: Callable[[], Iterable] = None, negative_data_from: Callable[[], Iterable] = None, allow_none: bool = True, required: bool = False, default: Any = None)

        :param Any validate: Data validator
        :param Callable[[], Iterable] positive_data_from: Function that returns a tuple of positive data
        :param Callable[[], Iterable] negative_data_from: Function that returns a tuple of negative data
        :param bool allow_none: ``True`` if the field can accept the value ``None``
        :param bool required: ``True`` if the field is required
        :param Any default: Default value

        Initializes an instance of a class

    .. py:method:: positive()

        Generates a common set of positive values for all internal field types

    .. py:method:: negative()

        Generates a common set of negative values for all internal field types

    .. py:method:: generate(length: int)

        :raises NotImplemented: If a method is not implemented in iterable data types when using a validator :py:class:`Length'

    .. py:method:: get_step()

        :raises NotImplemented: If the method is not implemented in numeric data types when using a validator :py:class:`Range`

    .. py:method:: get_other_value(value: Any)

        :raises NotImplemented: If the method is not implemented in the data type when using validators :py:class:`Equal`, :py:class:`OneOf`, :py:class:`NoneOf`

    .. py:method:: _register(for_register: Union[Any, List[Any]])

        :param Union[Any, List[Any]] for_register: Field value or list of values

        Stores ``for_register`` in the list of field values

    .. note::
        When creating your own numeric data types, implement their method :py:method:`get_precision`

    .. note::
        When creating your own iterable data types, implement their method :py:method:`generate`

    Class :py:class:`Field` is the base class for all internal data types

    Example:

    .. code-block:: python

        from sgen import fields


        class MyType(fields.Field)

            def positive(self):
                super().positive()

                if self.positive_data_from is not None:
                    return self.values

                if not self.validators:
                    self._register(None)  # Add a valid type value

                return self.values

            def negative(self):
                super().negative()

                if self.negative_data_from is not None:
                    return self.values

                self._register('None')  # Add a value that is not an instance of your data type

                return self.values

            def get_other_value(self, value: int) -> int:
                if value is None:
                    return MyType
                return MyType + 1


.. py:class:: String()

    .. py:method:: positive()

        :rtype: List[Union[None, Missing, str]]

        Generates a set of positive values for a type :py:class:`String`

    .. py:method:: negative()

        :rtype: List[Union[None, Missing, str, int]]

        Generates a set of negative values for a type :py:class:`String`

    .. py:method:: generate(length: int)

        :param int length: Length of the generated string
        :rtype: str

        Generates a string of the specified length.

    .. py:method:: get_other_value(value: Optional[str])

        :param str value: Unwanted string value
        :rtype: str

        Returns a value of the same type as ``value``, but not equal to ``value``


    Class :py:class:`String` is a representation of string data types

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class User(SGen)
            name = fields.String(allow_none=False)
            address = fields.String(
                validate=validate.Equal(comparable='Pepega street')
            )


.. py:class:: Integer()

    .. py:method:: __init__(step: int = 1, *args, **kwargs)

        :param int step: Step to generate values


    .. py:method:: positive()

        :rtype: List[Union[None, Missing, int]]

        Generates a set of positive values for a type :py:class:`Integer`

    .. py:method:: negative()

        :rtype: List[Union[None, Missing, int, str]]

        Generates a set of negative values for a type :py:class:`Integer`

    .. py:method:: get_step()

        :rtype: int

        Returns the step

    .. py:method:: get_other_value(value: Optional[int])

        :param int value: Undesired number value
        :rtype: int

        Returns a value of the same type as value, but not equal to value


    Class :py:class:`Integer` is a representation of an integer data type

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class User(SGen)
            age = fields.Integer(validate=validate.Range(min=21))


.. py:class:: Float()

    .. py:method:: __init__(step: float = 1, *args, **kwargs)

        :param int step: Step to generate values

    .. py:method:: positive()

        :rtype: List[Union[None, Missing, float]]

        Generates a set of positive values for a type :py:class:`Float`

    .. py:method:: negative()

        :rtype: List[Union[None, Missing, float, str]]

        Generates a set of negative values for a type :py:class:`Float`

    .. py:method:: get_step()

        :rtype: float

        Returns the step

    .. py:method:: get_other_value(value: Optional[float])

        :param float value: Undesired number value
        :rtype: float

        Returns a value of the same type as ``value``, but not equal to ``value``


    Class :py:class:`Float` is a floating point representation

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class User(SGen)
            balance = fields.Float(
                validate=validate.Range(min=0),
                step=0.0001
            )


.. py:class:: Boolean()

    .. py:method:: positive()

        :rtype: List[Union[None, Missing, bool]]

        Generates a set of positive values for a type :py:class:`Boolean`

    .. py:method:: negative()

        :rtype: List[Union[None, Missing, bool, str]

        Generates a set of negative values for a type :py:class:`Boolean`

    .. py:method:: get_other_value(value: Optional[bool])

        :param bool value: Undesired number value
        :rtype: bool

        Returns a value of the same type as ``value``, but not equal to ``value``

    Class :py:class:`Boolean` is a representation of the boolean data type

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class User(SGen)
            is_admin = fields.Boolean()


.. py:class:: DateTime()

    .. py:method:: __init__(step: timedelta = timedelta(days=1), *args, **kwargs)

        :param int step: Step to generate values

    .. py:method:: positive()

        :rtype: List[Union[None, Missing, datetime]]

        Generates a set of positive values for a type :py:class:`DateTime`

    .. py:method:: negative()

        :rtype: List[Union[None, Missing, datetime, str]]

        Generates a set of negative values for a type :py:class:`DateTime`

    .. py:method:: get_other_value(value: Optional[datetime])

        :param datetime value: Undesired number value
        :rtype: datetime

        Returns a value of the same type as ``value``, but not equal to ``value``

    .. py:method:: get_step()

        :rtype: timedelta

        Returns the step


    Class :py:class:`DateTime` is a representation of the data type datetime

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class User(SGen)
            created_at = fields.DateTime()


.. py:class:: Date()

    .. py:method:: __init__(step: timedelta = timedelta(days=1), *args, **kwargs)

        :param int step: Step to generate values

    .. py:method:: positive()

        :rtype: List[Union[None, Missing, date]]

        Generates a set of positive values for a type :py:class:`Date`

    .. py:method:: negative()

        :rtype: List[Union[None, Missing, date, str]]

        Generates a set of negative values for a type :py:class:`Date`

    .. py:method:: get_other_value(value: Optional[date])

        :param date value: Undesired number value
        :rtype: date

        Returns a value of the same type as ``value``, but not equal to ``value``

    .. py:method:: get_step()

        :rtype: timedelta

        Returns the step


    Class :py:class:`Date` is a date representation

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class User(SGen)
            birth_date = fields.Date()


.. py:class:: Collection()

    .. py:method:: __init__(data_type: Union[FieldABC, 'SGen'], *args, **kwargs)

        :param Union[FieldABC, 'SGen'] data_type: Collection data type

    .. py:method:: _register(for_register: Union[Any, List[Any]])

        :param Union[Any, List[Any]] for_register: Logged value or list of logged values

        Adds a new value/values to the field's list of values if it is not already present
        Additionally, it clears lists of the value ``Missing``, since doing this at the class level :py:class:`SGen` is inconvenient

    .. py:method:: positive()

        :rtype: List[Any]

        Generates a set of positive values for a type :py:class:`Collection`

    .. py:method:: negative()

        :rtype: List[Any]

        Generates a set of negative values for a type :py:class:`Collection`

    .. py:method:: generate(length: int)

        :param int length: Length of the generated collection
        :rtype: List[Any]

        Generates a collection

    .. py:method:: get_other_value(value: Optional[list])

        :param list value: Undesired number value
        :rtype: list

        Returns a value of the same type as ``value``, but not equal to ``value``


    Class :py:class:`Collection` is a list representation

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class Storage(SGen)
            user_ids = fields.Collection(
                data_type=fields.Integer()
            )


.. py:class:: Nested()

    .. py:method:: __init__(data_type: 'SGen', *args, **kwargs)

        :param SGen data_type: Schema data type

    .. py:method:: positive()

        :return: dictionary generator

        Generates a set of positive values for a type :py:class:`Nested`

    .. py:method:: negative()

        :return: dictionary generator

        Generates a set of negative values for a type :py:class:`Nested`

    Class :py:class:`Nested` is an implementation of nested entities

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate

        class Wallet(SGen):
            currency = fields.String(
                validate=validate.OneOf(choices=['RUB', 'EU', '$']),
                required=True,
                allow_none=False,
            )
            amount = fields.Integer(
                validate=validate.Range(min=0),
                required=True,
                allow_none=False,
            )

        class User(SGen):
            wallet = fields.Nested(data_type=Wallet(), required=True)


Validators
----------

.. py:class:: Length()

    .. py:method:: __init__(min: int = None, max: int = None, min_inclusive: bool = True, max_inclusive: bool = True)

        :param int min: Minimum length
        :param int max: Maximum length
        :param bool min_inclusive: True, if you need to include ``min`` in the range of valid length values
        :param bool max_inclusive: True, if you need to include ``max`` in the range of valid length values

    .. py:method:: positive(data_type: Field)

        :param Field data_type: Type of data to be validated.
        :rtype: List[Any]

        Generates a positive data set according to the validation parameters.

    .. py:method:: negative(data_type: Field)

        :param Field data_type: Type of data to be validated.
        :rtype: List[Any]

        Generates a negative data set according to the validation parameters.

    Represents a collection or string length validator.

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class User(SGen):
            name = fields.String(
                validate=validate.Length(min=1, max=10)
            )

    .. note::
        For the validator to work correctly, the data type must implement the method ``generate`` of class :py:class:`Field`


.. py:class:: Range()

    .. py:method:: __init__(min: int = None, max: int = None, min_inclusive: bool = True, max_inclusive: bool = True)

        :param int min: Minimum range limit
        :param int max: Maximum range limit
        :param bool min_inclusive: True, if you need to include ``min`` in the range of acceptable values
        :param bool max_inclusive: True, if you need to include ``max`` in the range of acceptable values

    .. py:method:: _get_min(data_type: Field, positive: bool = True)

        :param Field data_type: Data type.
        :param bool positive: Positive or negative meaning.
        :return: Minimum range limit.

        Returns the minimum limit of a range

    .. py:method:: _get_max(data_type: Field, positive: bool = True)

        :param Field data_type: Data type.
        :param bool positive: Positive or negative meaning.
        :return: Maximum range limit.

        Returns the maximum limit of a range

    .. py:method:: positive(data_type: Field)

        :param Field data_type: Type of data to be validated.
        :rtype: List[Any]

        Generates a positive data set according to the validation parameters.

    .. py:method:: negative(data_type: Field)

        :param Field data_type: Type of data to be validated.
        :rtype: List[Any]

        Generates a negative data set according to the validation parameters.

    Represents a number value range validator.

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class User(SGen):
            age = fields.Integer(
                validate=validate.Range(min=18, max=100)
            )

    .. note::
        For the validator to work correctly, the data type must implement the method ``get_step`` of class :py:class:`Field`


.. py:class:: Equal()

    .. py:method:: __init__(comparable: Any)

        :param Any comparable: The value that a field will take in a positive data set

    .. py:method:: positive(data_type: Field)

        :param Field data_type: Type of data to be validated.
        :rtype: List[Any]

        Generates a positive data set according to the validation parameters.

    .. py:method:: negative(data_type: Field)

        :param Field data_type: Type of data to be validated.
        :rtype: List[Any]

        Generates a negative data set according to the validation parameters.

    Represents an equality validator

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class User(SGen):
            age = fields.Integer(
                validate=validate.Equal(comparable=999)
            )

    .. note::
        For the validator to work correctly, the data type must implement the method ``get_other_value`` of class :py:class:`Field`


.. py:class:: OneOf()

    .. py:method:: __init__(choices: List[Any])

        :param List[Any] choices: List of valid field values

    .. py:method:: positive(data_type: Field)

        :param Field data_type: Type of data to be validated.
        :rtype: List[Any]

        Generates a positive data set according to the validation parameters.

    .. py:method:: negative(data_type: Field)

        :param Field data_type: Type of data to be validated.
        :rtype: List[Any]

        Generates a negative data set according to the validation parameters.

    Represents a validator for selecting a valid value from a list

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class User(SGen):
            age = fields.String(
                validate=validate.OneOf(choices=['Pepega', 'Aboba', 'PSFP5'])
            )

    .. note::
        For the validator to work correctly, the data type must implement the method ``get_other_value`` of class :py:class:`Field`


.. py:class:: NoneOf()

    .. py:method:: __init__(invalid_values: List[Any])

        :param List[Any] invalid_values: List of not valid field values

    .. py:method:: positive(data_type: Field)

        :param Field data_type: Type of data to be validated.
        :rtype: List[Any]

        Generates a positive data set according to the validation parameters.

    .. py:method:: negative(data_type: Field)

        :param Field data_type: Type of data to be validated.
        :rtype: List[Any]

        Generates a negative data set according to the validation parameters.

    Allows you to specify not valid values for a field

    Example:

    .. code-block:: python

        from sgen import fields, SGen, validate


        class User(SGen):
            is_admin = fields.Bool(
                validate=validate.NoneOf(invalid_values=[False])
            )

    .. note::
        For the validator to work correctly, the data type must implement the method ``get_other_value`` of class :py:class:`Field`
