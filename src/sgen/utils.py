from inspect import isgeneratorfunction, isgenerator


class Missing:
    """Represents an instance of a missing field"""

    def __repr__(self):
        return "<sgen.missing>"


class ValuesStorage(list):
    """Represents storage for field values"""

    def __contains__(self, item):
        present = list(filter(
            lambda value: type(value) == type(item) and value == item,
            self
        ))

        return bool(present)


def is_generator(obj) -> bool:
    """Returns True if obj is a generator"""

    return isgeneratorfunction(obj) or isgenerator(obj)


def is_iterable_but_not_string(obj) -> bool:
    """Returns True if obj is iterable but not a string"""

    return (hasattr(obj, "__iter__") and not hasattr(obj, "strip")) or is_generator(obj)
