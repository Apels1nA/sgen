.. _quickstart:

Quickstart
==========

In this guide will cover:

* :ref:`schema-definition`
* :ref:`data-generation`

.. _model-definition:

Create a class that describes your entity and inherit from the :py:class:`SGen` class

.. code-block:: python

    from sgen import SGen, fields


    class User(SGen):
        name = fields.String(required=True)
        age = fields.Integer(allow_none=False)

SGen contains many :ref:`fields`

.. _data-generation:

.. code-block:: python

    from pprint import pprint

    from sgen import SGen, fields


    class Pet(SGen):
        name = fields.String()


    class User(SGen):
        name = fields.String()
        pet = fields.Nested(Pet(), required=True)


    def main():
        datasets = list(User().positive())

        pprint(datasets, indent=2)


    if __name__ == '__main__':
        main()

    # [ {'name': None, 'pet': {'name': None}},
    #   {'name': None, 'pet': {}},
    #   {'name': None, 'pet': {'name': 'fszxSnf'}},
    #   {'pet': {'name': None}},
    #   {'pet': {}},
    #   {'pet': {'name': 'RzGTdNzhr'}},
    #   {'name': 'ttr', 'pet': {'name': None}},
    #   {'name': 'ttr', 'pet': {}},
    #   {'name': 'ttr', 'pet': {'name': 'ZpvMOyR'}}]
