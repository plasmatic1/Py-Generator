class Xorrer:
    def __init__(self, input_file, output_file, debug=False):
        """
        Xorrer class.  Tool for encrypting input
        :param input_file:
        :param output_file:
        :param debug:
        """
        with open(input_file) as f:
            self.input = f.read().split('\n')
        with open(output_file) as f:
            self.output = f.read().split('\n')
        # TODO: Implement xorrer

