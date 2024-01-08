SGen
======

Your welcome <3

Description
-----------

Sgen is a tool for generating test data structures in Python.

.. code-block:: python

    from pprint import pprint

    from sgen import Sgen, fields


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


In short, SGen can be used to:

* Generating positive data structures
* Generating negative data structures
* Checking the functionality of data validation at the application input

Get It Now
----------

.. code-block:: console

    pip install sgen

Documentation
-------------

Full documentation is available at `here <https://sgen.readthedocs.io/>`_

Requirements
------------

- Python >= 3.8

Project Links
-------------

* `Repo <https://github.com/Apels1nA/sgen>`_
* `Docs <https://sgen.readthedocs.io/en/latest/index.html>`_
* `Changelog <https://sgen.readthedocs.io/en/latest/changelog.html>`_
* `Issues <https://github.com/Apels1nA/sgen/issues>`_

License
-------

* ``MIT`` licensed.
