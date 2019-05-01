SKIP_FIELDS = {'__init__', '__str__', '__repr__'}


def wrap_func(func):
    def wrapper(self, *args, **kwargs):
        delattr()

    return wrapper


def mutable_type(type_):
    class Mutable:
        wrapping = type_

        def __init__(self, value):
            self.value = value

        def __str__(self):
            return '<Mutable enclosing "%s">' % self.value

        def __repr__(self):
            return self.__str__()

    for k, v in type_.__dir__.items():
        if k not in SKIP_FIELDS:
            setattr(Mutable, k, wrap_func(v))

    return Mutable
