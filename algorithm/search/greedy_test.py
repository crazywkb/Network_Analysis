import networkx as nx
from algorithm.community.community_detection import louvain
from utils.count_entropy import count_resistance
from utils.graph_IO import read_gml
import time

class Greedy(object):
    def __init__(self, graph, func=louvain, func_args=dict()):
        self.graph = graph
        self.func = func
        self.func_args = func_args
        self.available_edges = None

    def get_available_edges(self, modules):
        """
        get available edges which can be used in anonymize() function
        :param modules: dict, modules of graph
        :return: None
        """
        inside_edges = set()
        for module in modules.values():
            sub_graph = nx.complete_graph(module)
            inside_edges.update(sub_graph.edges)

        module_cross_edges = nx.complete_graph(self.graph.nodes).edges - inside_edges
        self.available_edges = module_cross_edges - self.graph.edges
        print("You get %d edges available."%(len(self.available_edges)))

    def anonymize(self, sum_of_edge=None, added_edges=None, interval=1):
        assert isinstance(sum_of_edge, int) or isinstance(added_edges, list)
        modules = self.func(self.graph, **self.func_args)
        self.get_available_edges(modules)
        # Todo: remain to finish.


if __name__ == '__main__':
    temp_graph = read_gml("../../samples/dolphins.gml")
    greedy = Greedy(temp_graph)
    temp_modules = louvain(temp_graph)

    start_time = time.time()
    for i in range(200):
        greedy.get_available_edges(temp_modules)
    end_time = time.time()

    print("Total cost: " + str(end_time - start_time))