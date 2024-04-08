from inspect import getmembers
from typing import List

from sgen.fields import Field
from sgen.dto import SchemaField
from sgen.utils import Missing


__all__ = ["SGen"]


class SGen:
    """Class for generating test data structures."""

    def fields(self, is_positive: bool) -> List[SchemaField]:
        """
        Returns a list of schema fields and data generators for them.

        :param is_positive: True if you need to return positive generators.
        :return: List of SchemaField.
        """

        method = 'positive' if is_positive else 'negative'

        schema_fields = getmembers(
            self,
            lambda field: isinstance(field, Field)
        )

        return [
            SchemaField(attr_name=field[0], data_generator=getattr(field[1], method))
            for field in schema_fields
        ]

    def _generate(self, fields: List[SchemaField]):
        """
        Generates a Cartesian product of field values.

        :param fields: List of fields.
        :return: Generator.
        """

        if len(fields) == 1:
            for value in fields[0].data_generator():
                yield [(fields[0].attr_name, value)]
        else:
            for value in fields[0].data_generator():
                for rest in self._generate(fields=fields[1:]):
                    yield [(fields[0].attr_name, value)] + rest

    def positive(self):
        """
        Generates a set of positive test data.

        :return: Dictionary generator.
        """

        for dataset in self._generate(fields=self.fields(is_positive=True)):
            yield dict(filter(
                lambda field_value: not isinstance(field_value[1], Missing),
                dataset
            ))

    def negative(self):
        """
        Generates a set of negative test data.

        :return: List of dictionaries.
        """

        positive_generators = self.fields(is_positive=True)
        negative_generators = self.fields(is_positive=False)

        for n_gen in negative_generators:
            fields = [n_gen]
            for p_gen in positive_generators:
                if p_gen.attr_name == n_gen.attr_name:
                    continue
                fields.append(p_gen)

            for dataset in self._generate(fields=fields):
                yield dict(filter(
                    lambda field_value: not isinstance(field_value[1], Missing),
                    dataset
                ))
