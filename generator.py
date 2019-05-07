import param_parser
import util.seq
import util.graph
import random


def insert_module(recipient, module):
    """
    Inserts the module into the recipient (another module).  This is akin to doing "from module import *" in the recipient python file
    :param recipient: The recipient module
    :param module: The module to insert
    :return:
    """
    for attr, val in module.__dict__.items():
        if not (attr.startswith('__') and attr.endswith('__')):  # Magic attributes are skipped
            setattr(recipient, attr, val)


class Generator:
    def __init__(self, file, **kwargs):
        """
        Initializes generator object
        :param file: The generator module, it has to be a path to a .py file
        :param auto_import: Whether the generator will automatically import certain functionality into the generator source file.  Defaults to True
        """
        self.generator = __import__(file.split('.')[0])
        self.data = ''

        for func in [self.wobj, self.wline, self.wf, self.wseq]:  # These functions are required to generate data
            setattr(self.generator, func.__name__, func)

        # Auto-importing functions
        # TODO: Other library functions
        if kwargs.get('auto_import', True):
            insert_module(self.generator, util.seq)
            insert_module(self.generator, util.graph)
            insert_module(self.generator, random)

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
        :param sep: The separator
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

        self.data = ''
        self.generator.run()
        return self.data
