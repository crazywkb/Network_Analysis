import networkx as nx
class Greedy(object):
    def __init__(self, graph, modules):
        self.graph = graph.copy()
        self.modules = modules
