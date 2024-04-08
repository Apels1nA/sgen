.. custom_data_types:

Custom data types
======================

To create your own data type, inherit a new class from :py:class:`Field`

.. note::
    Implement the :func:`~Field.generate` method if you use the :py:class:`Length` validator along with your data type

.. note::
    Implement the :func:`~Field.get_step` method if you use the :py:class:`Range` validator along with your data type

.. note::
    Implement the :func:`~Field.get_other_value` methods if you use the :py:class:`Equal`, :py:class:`OneOf`, :py:class:`NoneOf` validator along with your data type

Example:

    .. code-block:: python

        from sgen import fields


        class MyInt(fields.Field)

            def set_positive_values(self):
                self._register(1)  # Add a valid type value

            def set_negative_values(self):
                self._register('not_int')  # Add a value that is not an instance of your data type

            def get_other_value(self, value: int) -> int:
                if value is None:
                    return 1
                return value + 1

            def __add__():
                pass

            def __sub__():
                pass
