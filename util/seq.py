from random import *


class Unique:
    OPERATIONS = ('seq', 'next', 'readd')

    def __seq0(self, len_):
        sz = len(self.vals)
        ret = self.vals[sz - len_:sz]
        del self.vals[sz - len_:]
        return ret

    def __seq1(self, len_):
        return [self.next() for _ in range(len_)]

    def __next0(self):
        return self.vals.pop()

    def __next1(self):
        ret = choice(self.range)
        while ret in self.used:
            ret = choice(self.range)
        self.used.add(ret)
        return ret

    def __readd0(self, val):
        self.vals.append(val)
        idx = randint(0, len(self.vals) - 2)
        self.vals[-1], self.vals[idx] = self.vals[idx], self.vals[-1]

    def __readd1(self, val):
        self.used.remove(val)

    def seq(self, len_):
        """
        Creates a unique sequence of length `len_`
        :param len_: The length of the sequence
        :return: The sequence
        """
        pass

    def next(self):
        """
        Generates the next random unique number
        :return: The number generated
        """
        pass

    def readd(self, val):
        """
        Reinserts an already removed value into the pool of available values.  Assumes that the value is within the
        range of the generator
        :param val: The value to add back
        :return:
        """
        pass

    def __init__(self, range_, mode=0):
        """
        A Unique sequence (and number) generator.  The generator supports two different modes for different types of data
        sets.
        Mode 0: First creates all possible values, then looks through that list
        Mode 1: Picks random numbers until a unique one is found
        :param range_: The range of numbers available
        :param mode: The generation mode, defaults to 0
        """
        self.range = range_
        self.mode = mode

        if not self.mode:
            self.vals = list(range_)
            shuffle(self.vals)
        else:
            self.used = set()

        # Adding operations
        for op in Unique.OPERATIONS:
            setattr(self, op, getattr(self, '_%s__%s%d' % (Unique.__name__, op, self.mode)))
