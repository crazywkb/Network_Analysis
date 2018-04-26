import networkx as nx
from algorithm.community.community_detection import louvain
from utils.count_entropy import count_resistance


class Greedy(object):
    def __init__(self, graph, func=louvain):
        self.graph = graph.copy()
        self.community_detection = func
        self.initial_modules = self.community_detection(graph)
        self.diff_edges = None

    def serarch(self):
        full_edges = {(i, j) for i in range(self.graph.number_of_nodes()) for j in range(i + 1, self.graph.number_of_nodes())}
        self.diff_edges = list(full_edges - self.graph.edges)
        resistence = 0

        while 1:
            max = 0
            for edge in self.diff_edges:
                self.graph.add_edge(*edge)
                # Todo: find the edge which can max the resistence count by count_resistence()