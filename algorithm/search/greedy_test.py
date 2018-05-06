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
        inside_edges = set()
        for module in modules.values():
            sub_graph = self.graph.subgraph(module)
            inside_edges.update(sub_graph.edges)

        outside_edges = nx.complete_graph(self.graph.nodes)

        self.available_edges = outside_edges - self.graph.edges - inside_edges
        print(len(self.available_edges), len(outside_edges), len(inside_edges))


if __name__ == '__main__':
    greedy = Greedy(read_gml("../../samples/dolphins.gml"))
    temp_modules = louvain(nx.karate_club_graph())
    start_time = time.time()
    for i in range(200):
        greedy.get_available_edges(temp_modules)
    end_time = time.time()
    print("Total cost: " + str(end_time - start_time))