.. _fields:

Fields
======

Scheme fields are intended to describe the desired result. When you create a schema class,
fields are declared as its attributes.

Field initialization arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parameters accepted by all field types and their default values:

* ``allow_none = True`` -- Allow null values
* ``required = True`` -- Is the field required
* ``default = True`` -- Any value that will be used by default
* ``validate = None`` -- None type or validator
* ``positive_data_from = None`` -- A function object that will return a list of positive values or None
* ``negative_data_from = None`` -- A function object that will return a list of negative values or None

.. note::
     Some field types such as :py:class:`Integer`, :py:class:`Float`, :py:class:`Collection` and :py:class:`Nested`
     accept an additional argument. For :py:class:`Integer` and :py:class:`Float` this argument is ``precision``.
     It is responsible for the minimum number step that will be used when generating negative values
     validator :py:class:`Range`. For the :py:class:`Collection` and :py:class:`Nested` types, this parameter is ``data_type``.
     It accepts a nested data type. For :py:class:`Collection` - the data type inside the collection,
     for :py:class:`Nested` - nested schema (class instance inherited from :py:class:`SGen`)

.. note::
    When using the ``positive_data_from`` and ``negative_data_from`` parameters their values
    will completely replace the result of generating the ``positive()`` and ``negative`` methods

String field
^^^^^^^^^^^^

Represents a string data type. Generates random strings with the ability to install
minimum/maximum length by using the :py:class:`Length` validator

.. code-block:: python

    from sgen import SGen, validate, fields

    class User(SGen):
        name = fields.String(
            validate=validate.Length(
                min=10,
                max=100,
                min_inclusive=True,
                max_inclusive=False,
            )
        )

    user_sgen = User()
    user_sgen.positive()  # Returns positive data generator
    user_sgen.negative()  # Returns negative data generator

The ``min_inclusive`` and ``max_inclusive`` parameters are responsible for including ``min/max`` in the range of acceptable values

Integer Field
^^^^^^^^^^^^^

Represents an integer data type. Generates random numbers with the ability to set
min/max value by using :py:class:`Range` validator

Additionally, it includes the ``precision`` parameter, which is responsible for the step when generating negative values
or positive, provided that at least one of the ``...inclusive`` parameters is ``False``.

.. note::
    I don’t see any obvious cases of using the ``precision`` parameter for the ``Integer`` type, I left it for flexibility.

.. code-block:: python

    from sgen import SGen, validate, fields

    class User(SGen):
        age = fields.Integer(
            validate=validate.Range(
                min=10,
                max=100,
                min_inclusive=True,
                max_inclusive=False,
            )
        )

The ``min_inclusive`` and ``max_inclusive`` parameters are responsible for including ``min/max`` in the range of acceptable values


Float field
^^^^^^^^^^^

Represents floating point numbers. Generates settable random floating point numbers
min/max value by using :py:class:`Range` validator

Additionally, it includes the ``precision`` parameter, which is responsible for the step when generating negative values
or positive, provided that at least one of the ``...inclusive`` parameters is ``False``.

.. code-block:: python

    from sgen import SGen, validate, fields

    class User(SGen):
        balance = fields.Float(
            validate=validate.Range(
                min=10,
                max=100,
                min_inclusive=True,
                max_inclusive=False,
            )
        )

The ``min_inclusive`` and ``max_inclusive`` parameters are responsible for including ``min/max`` in the range of acceptable values

Boolean field
^^^^^^^^^^^^^

Represents a Boolean data type.

.. code-block:: python

    from sgen import SGen, validate, fields

    class User(SGen):
        age = fields.Float(
            validate=validate.Equal(
                comparable=True
            )
        )

DateTime and Date field
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Represents time data types.

.. code-block:: python

    from sgen import SGen, validate, fields

    class User(SGen):
        created_at = fields.DateTime()
        birth_date = fields.Date()

Collection field
^^^^^^^^^^^^^^^^

Represents lists.

.. code-block:: python

    from sgen import SGen, validate, fields

    class User(SGen):
        numbers = fields.List(
            data_type=fields.Integer()
        )

Accepts the argument ``data_type`` which must be an inheritor of the :py:class:`Field` class

Nested field
^^^^^^^^^^^^

Represents nested schemas.

.. code-block:: python

    from sgen import SGen, validate, fields


    class Pet(SGen):
        name = fields.String()


    class User(SGen):
        pet = fields.Nested(
            Pet(),
            required=True,
        )

Accepts the argument ``data_type`` which must be an inheritor of the class :py:class:`SGen`
