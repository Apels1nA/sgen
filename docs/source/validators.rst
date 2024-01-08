.. _validators:

Validators
======

Validators are designed to configure generation parameters.

Length validator
^^^^^^^^^^^^^^^^

Length validator for iterable data types.

.. code-block:: python

    class User(SGen):
        name = fields.String(
            validate=validate.Length(
                min=10,
                max=100,
                min_inclusive=True,
                max_inclusive=False,
            )
        )

.. note::
    Compatible with :py:class:`List` and :py:class:`String`. For correct operation of this validator with a specific data type
    the latter should have a ``generate`` method that takes a single parameter ``length: int``
    and returns a collection of ``length``.

Range validator
^^^^^^^^^^^^^^^^

Value range validator for numeric data types.

.. code-block:: python

    class User(SGen):
        age = fields.Integer(
            validate=validate.Range(
                min=18,
            )
        )

.. note::
    Compatible with :py:class:`Integer` and :py:class:`Float`. For correct operation of this validator with a specific data type
    the latter must have a ``get_precision`` method that takes no parameters and returns the number step.

Equal validator
^^^^^^^^^^^^^^^^

Equality validator. For positive generations, the comparable value will be included.
On the day of negative generations, the value ``comparable`` will be excluded.

.. code-block:: python

    class User(SGen):
        name = fields.String(
            validate=validate.Equal(comparable='Aboba')
        )

.. note::
    Compatible with all standard data types. For correct operation of this validator with a specific data type
    the latter must have a ``get_other_value`` method which takes a value parameter and returns a value of the same type
    but not equal to value

OneOf validator
^^^^^^^^^^^^^^^^

Selection validator. For positive value generation, ``choices`` will be included.
Days of negative generation of ``choices`` values will be excluded.

.. code-block:: python

    class User(SGen):
        address = fields.String(
            validate=validate.OneOf(choices=['Pepega street', 'Uganda city'])
        )

.. note::
    Compatible with all standard data types. For correct operation of this validator with a specific data type
    the latter must have a ``get_other_value`` method which takes a value parameter and returns a value of the same type
    but not equal to value

NoneOf validator
^^^^^^^^^^^^^^^^

The opposite of choice validators. For positive value generation, ``invalid_values`` will be excluded.
Days of negative generation values ``invalid_values`` will be included.

.. code-block:: python

    class User(SGen):
        name = fields.String(
            validate=validate.NoneOf(invalid_values=['Kirill', 'Zlatoslava'])
        )

.. note::
    Compatible with all standard data types. For correct operation of this validator with a specific data type
    the latter must have a ``get_other_value`` method which takes a value parameter and returns a value of the same type
    but not equal to value
