import yaml
import generator
import os


class Parser:
    def __init__(self, data_file):
        """
        Initializes parser
        :param data_file: The configuration file (should be a .yml file)
        """
        with open(data_file) as f:
            data = f.read()
        self.data = yaml.safe_load(data)
        self.generator = generator.Generator(self.data['input_generator'],
                                             **(self.data['generator_args'] if 'generator_args' in self.data else {}))

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
            print('Missing generator argument or output file format argument, no output will be created...')

        # Encrypting (Xorring) queries for online-only problems

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
                silent_remove(in_format % i, 'Could not find %path')
                silent_remove(out_format % i, 'Could not find %path')

            counter += amount


def silent_remove(path, msg=None):
    """
    os.remove() but does not have a brain aneurysm when a file doesn't exist

    :param path: Path to remove
    :param msg: Optional message (%path substituted with file name) to output when file doesn't exist
    :return: None
    """

    try:
        os.remove(path)
    except FileNotFoundError:
        if msg:
            print(msg.replace('%path', path))
