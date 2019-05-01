import random
import re


def process_param(param):
    """
    Processes the value in the `vars` section in a case config.  Generally they are kept untouched except for these
    extended data types

    x~y : Random (uniform) number between `x` and `y` (An integer if both `x` and `y` are integers, otherwise it is a float)
    x:y : Range from `x` to `y` with +1 increment.  Note that these are standard python ranges
    x:y:z : Range from `x` to `y` with `+z` increment

    :param param: The parameter to process
    :return: The processed parameter
    """

    if isinstance(param, str):
        spl = param.split('~')

        if len(spl) == 2:
            if _is_int(spl[0]) and _is_int(spl[1]):
                return random.randint(int(spl[0]), int(spl[1]))
            elif _is_number(spl[0]) and _is_number(spl[1]):
                return random.uniform(float(spl[0], float(spl[1])))

        spl = param.split(':')

        if 2 <= len(spl) <= 3:
            if all(spl, _is_int):
                return range(*map(int, spl))

        return param
    return param


def _is_number(str_):
    """
    Checks if str_ is a number (either float or int)
    :param str_: The string to check
    :return: Whether it is a float
    """

    return _is_int(str_) or _is_float(str_)


def _is_float(str_):
    """
    Checks if str_ is a float
    :param str_: The string to check
    :return: Whether it is a float
    """

    return bool(re.match('[+-]?\d+\.\d*$', str_))


def _is_int(str_):
    """
    Checks if str_ is an int
    :param str_: The string to check
    :return:
    """

    return bool(re.match('[+-]?\d+$', str_))
