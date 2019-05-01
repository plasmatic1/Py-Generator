import param_parser


class Generator:
    def __init__(self, file):
        """
        Initializes generator
        :param file: The source generator, it has to be a path to a .py file
        """
        self.generator = __import__(file.split('.')[0])
        self.data = ''
        self.libs = [self.wobj, self.wline, self.wf, self.wseq]

    def wobj(self, arg):
        """
        Writes an object + \n to the data
        :param arg: The object to write
        :return:
        """
        self.data += str(arg) + '\n'

    def wseq(self, seq, sep=' '):
        """
        Writes a sequence to the test data separated by a delimiter (with a space by default)
        :param seq: The sequence to write
        :param sep: THe separator
        :return:
        """
        self.data += sep.join(map(str, seq))

    def wline(self, *objs, sep=' '):
        """
        Same as wobj except it supports a variable amount of arguments and a separator
        :param sep: The separator, defaults to ' '
        :param objs: The objects to write
        :return:
        """
        self.data += sep.join(map(str, objs)) + '\n'

    def wf(self, fmt, *args):
        """
        C-style printf but it writes to test data
        :param fmt: The format
        :param args: The arguments
        :return:
        """
        self.data += fmt % args

    def run(self, vars_):
        """
        Runs the generator with the supplied variables
        :param vars_: A dict of all the variables being supplied
        :return: The generated test data, as a string
        """

        # Setting variables
        for key, val in vars_.items():
            setattr(self.generator, key, param_parser.process_param(val))

        # TODO: Other library functions

        for func in self.libs:
            setattr(self.generator, func.__name__, func)

        self.data = ''
        self.generator.run()
        return self.data
