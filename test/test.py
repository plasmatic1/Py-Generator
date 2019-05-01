import unittest
import config_parser
import param_parser


def test_data(file_name):
    with open(file_name) as f:
        return map(int, f.read().strip().split())


class TestConfig(unittest.TestCase):
    def test_config(self):
        with open('sample_config.yml') as f:
            config_data = f.read()
        config = config_parser.Parser(config_data)
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


if __name__ == '__main__':
    unittest.main()
