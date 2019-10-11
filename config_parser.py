import yaml
from tool import generator
import os


class Parser:
    def __init__(self, data_file, debug_output_stream=None):
        """
        Initializes parser
        :param debug_output_stream: The I/O stream where debug info will be sent, or none if not specified
        :param data_file: The configuration file (should be a .yml file)
        """
        with open(data_file) as f:
            data = f.read()
        self.data = yaml.safe_load(data)
        self.generator = generator.Generator(self.data['input_generator'],
                                             **(self.data['generator_args'] if 'generator_args' in self.data else {}))
        self.debug_output_stream = debug_output_stream
        self.__case_count = -1

    def make_cases(self):
        """
        Uses the config to generate cases.  Case files will be created
        :return: None
        """
        counter = 1
        for case in self.data['cases']:
            amount = case.get('amount', 1)
            vars_ = case.get('vars', {})

            for i in range(amount):
                with open(self.data['input_file_format'] % (counter + i), 'w') as f:
                    f.write(self.generator.run(vars_))

            counter += amount

        # Output Generation
        if self.data.get('output_file_format', None) and self.data.get('output_generator', None):
            file_format = self.data['output_file_format']
            for i in range(1, counter):
                with open(file_format % i, 'w') as f:
                    pass  # TODO: Output generator.  Use PyTester run.py for this
        else:
            self.debugf('Missing generator argument or output file format argument, no output will be created...')

    def xor_cases(self):
        raise NotImplementedError  # TODO: Implement xorring of files

    def validate_cases(self):
        raise NotImplementedError  # Todo: Implement validation structure

    def delete_cases(self):
        """
        Deletes generated case files.  Mostly for testing
        :return: None
        """
        counter = 1
        in_format = self.data['input_file_format']
        out_format = self.data['output_file_format']

        for case in self.data['cases']:
            amount = case.get('amount', 1)
            for i in range(counter, counter + amount):
                if not silent_remove(in_format % i):
                    self.debugf('Could not find %s', in_format % i)
                if not silent_remove(out_format % i):
                    self.debugf('Could not find %s', out_format % i)

            counter += amount

    @property
    def case_count(self):
        """
        Getter for case_count property.  Returns -1 if not initialized
        :return: The # of cases
        """
        if self.__case_count == -1:
            raise AttributeError('Case count not initialized! (make_cases needs to be called first)')
        return self.__case_count

    @case_count.setter
    def set_case_count(self, cnt):
        """
        Default setter for case_count
        :param cnt: The new case_count
        :return:
        """
        self.__case_count = cnt

    def debugf(self, format_, *args, end='\n'):
        """
        Similar to printf but writes to the debug stream.  Note that an ending is added to the format, defaults to '\n'
        :param format_: The format
        :param args: The arguments (what you would find in printf)
        :param end: The 'end' that's appended after the format.  Defaults to '\n'
        :return:
        """
        if self.debug_output_stream:
            self.debug_output_stream.write(format_ % args + end)


def silent_remove(path):
    """
    os.remove() but does not have a brain aneurysm when a file doesn't exist.  Returns whether the command succeeded
    :param path: Path to remove
    :return: True if successful, False if the file was not found
    """
    try:
        os.remove(path)
        return True
    except FileNotFoundError:
        return False
