from collections import namedtuple

RangeExt = namedtuple('RangeExt', 'range inverted')


class IntMatcher:
    def __init__(self, expr):
        """
        A pattern matcher for integer values.  It supports the following tokens, separated by commas.  Note that whitespace does not matter.
        `x`: Matches a single integer value
        `x`:`y`: Matches the range from x to y-1 inclusive, where x and y are integers
        `x`:`y`:`z`: Similar to the previous token, but matches with a step value z also (i.e. 1:10:2 would match (1, 3, 5, 7, 9))
        ^`x`: Matches the opposite of whatever value is matched by token `x` (where `x` is a valid token).  Note that you cannot chain multiple `^` tokens
        :param expr: The expression that the matcher is constructed with
        """
        self.ranges = []
        for block in expr.split(','):
            block = block.strip()
            if block.startswith('^'):
                inv = True
                block = block[1:]
            else:
                inv = False

            spl = block.split(':')
            if len(spl) > 1:
                self.ranges.append(RangeExt(range(*map(int, spl)), inv))
            else:
                self.ranges.append(int(spl), inv)

    def __contains__(self, num):
        """
        Checks if the specified number matches the Integer Matcher.  This function runs in O(N) time, where N is the number of tokens in the matcher
        :param num: The number to check
        :return: Whether it matches or not
        """
        if not isinstance(num, int):
            raise ValueError('Number must be integer!')

        for range_ in self.ranges:
            if ((isinstance(range_, int) and num == range_.range) or
                    (num in range_.range)) ^ range_.inv:
                return True
        return False


class Queries:
    def __init__(self):
        self.type_generators = {}
        # TODO: Implement query generation (not sure how to do this really)
