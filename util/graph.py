from random import *


class InvalidEdgeError(Exception):
    pass


class Graph:
    def __init__(self, **kwargs):
        """
        Basic graph data type, currently supports the following arguments:
        N: The number of nodes
        M: The number of edges
        allow_duplicate: Whether the graph allows for duplicate edges.  Defaults to False
        allow_self_loop: Whether edges from node i to node i are allowed.  Defaults to False
        weighted: Whether the graph is weighted.  Defaults to False
        weights: If weighted is true, then this value must be a python `range` object
        :param kwargs: The arguments
        """
        self.used = set()
        self.edges = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_edge(self, a, b):
        """
        Adds edge between a and b.  If the graph is weighted, then it also attaches a weight.  This just skips some of the processing involved.
        If `a` and `b` do not meet the requirements of the graph, then an InvalidEdgeError will be thrown
        :param a: The first node
        :param b: The second node
        :return:
        """
        if getattr(self, 'allow_self_loop', False) and a == b:
            raise InvalidEdgeError('No self loops!')
        if getattr(self, 'allow_duplicate', False):
            if a > b:
                ta = b
                tb = a
            else:
                ta = a
                tb = b

            if (ta, tb) in self.used:
                raise InvalidEdgeError('Duplicate edge!')

            self.used.add((ta, tb))

        if getattr(self, 'weighted', False):
            self.edges.append((a, b, choice(self.weights)))
        self.edges.append((a, b))

    def generate(self):
        """
        Generate function
        :return: A list of tuples, the edges generated
        """
        while len(self.edges) < self.M:
            try:
                self.add_edge(randint(1, self.N), randint(1, self.N))
            except InvalidEdgeError:
                pass

        return self.edges


class Tree(Graph):
    def __init__(self, **kwargs):
        """
        A tree graph.  Note that `M` cannot be specified as an argument for this function
        :param kwargs: The arguments
        """
        super().__init__(**kwargs)
        if self.__class__ == Tree:  # Any initialization that doesn't want to be called by a subclass
            if hasattr(self, 'M'):
                raise ValueError('Trees can\'t have a variable amount of edges!')
            self.M = self.N - 1

    def generate(self):
        edge_a = list(range(1, self.N + 1))
        shuffle(edge_a)
        edge_b = []

        for i in edge_a:
            par = randint(1, self.N)
            while par == i:
                par = randint(1, self.N)

        for i in range(self.N - 1):
            self.add_edge(edge_a[i], edge_b[i])

        return self.edges


class ConnectedGraph(Tree):
    def __init__(self, **kwargs):
        """
        A fully connected graph
        :param kwargs: The arguments
        """
        super().__init__(**kwargs)

    def generate(self):
        super().generate()
        return Graph.generate(self)


class DAG(Graph):
    def __init__(self, **kwargs):
        """
        A Directed Acyclic Graph
        :param kwargs: The arguments
        """
        super().__init__(**kwargs)
        # TODO: Implement DAG Generation
