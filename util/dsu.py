class UnionFind:
    def __init__(self, size):
        """
        Disjoint Set (Union Find) data structure using the path compression optimization.  Implementation was tested on https://dmoj.ca/problem/ds2
        :param size: The size of the set, note that this is one-indexed
        """
        self.size = size
        self.par = [i for i in range(size + 1)]

    def root(self, node):
        """
        Finds the root of the node
        :param node: The node
        :return: The root of the node
        """
        if self.par[node] == node:
            return node
        self.par[node] = self.root(self.par[node])
        return self.par[node]

    def merge(self, node1, node2):
        """
        Merges the two nodes
        :param node1: Node 1
        :param node2: Node 2
        :return:
        """
        if node1 != node2:
            self.par[self.root(node2)] = self.root(node1)

    def same(self, node1, node2):
        """
        Checks if two nodes are part of the same set
        :param node1: Node 1
        :param node2: Node 2
        :return: Whether they are in the same set
        """
        return self.root(node1) == self.root(node2)