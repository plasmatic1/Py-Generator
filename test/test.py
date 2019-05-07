import unittest
import config_parser
import param_parser
import util.seq


def test_data(file_name):
    with open(file_name) as f:
        return map(int, f.read().strip().split())


class TestConfig(unittest.TestCase):
    def test_config(self):
        config = config_parser.Parser('sample_config.yml')
        config.make_cases()

        # Testing

        a, b = test_data('1.in')
        self.assertEqual(a, 1)
        self.assertEqual(b, 1)

        a, b = test_data('2.in')
        self.assertEqual(a, 15)
        self.assertEqual(b, 5)

        for i in range(3, 8):
            a, b = test_data('%d.in' % i)
            self.assertTrue(1 <= a <= 10)
            self.assertEqual(b, 100)

        config.delete_cases()

        # Test the auto_import function
        config = config_parser.Parser('sample_config2.yml') # TODO: Fix auto_import always importing even when set to false
        config.make_cases()
        config.delete_cases()


class TestIsNumber(unittest.TestCase):
    def test_is_int(self):
        cases = [
            ('1', True),
            ('2.', False),
            ('-1', True),
            ('12312313', True),
            ('-123.34', False),
            ('1af', False),
            ('b5abab', False),
            ('+123', True),
            ('-12-2', False),
            ('0', True),
            ('+12+2', False)
        ]

        for test, res in cases:
            self.assertEqual(param_parser._is_int(test), res,
                             'Failed test of number \'%s\'.  Expected %s' % (test, str(res)))

    def test_is_float(self):
        cases = [
            ('1.21', True),
            ('2.', True),
            ('-1', False),
            ('12312313', False),
            ('-123.34', True),
            ('1af', False),
            ('b5', False),
            ('+123.539', True),
            ('-12-2', False),
            ('0', False),
            ('+12+2', False)
        ]

        for test, res in cases:
            self.assertEqual(param_parser._is_float(test), res,
                             'Failed test of number \'%s\'.  Expected %s' % (test, str(res)))


class TestUnique(unittest.TestCase):
    RANGE = range(1, int(1e5))
    SEQ_LEN = 100
    RAND_CNT = 1000

    def __test(self, mode):
        gen = util.seq.Unique(TestUnique.RANGE, mode)
        seq = gen.seq(TestUnique.SEQ_LEN)
        used = set(seq)
        self.assertEqual(len(seq), len(used), 'Duplicate sequence!')
        self.assertEqual(len(seq), TestUnique.SEQ_LEN)

        for _ in range(TestUnique.RAND_CNT):
            v = gen.next()
            self.assertNotIn(v, used, 'Duplicate random!')
            used.add(v)

    def test_mode0(self):
        self.__test(0)

    def test_mode1(self):
        self.__test(1)


class TestGraph(unittest.TestCase):
    pass  # TODO: Implement graph unit testing


if __name__ == '__main__':
    unittest.main()
