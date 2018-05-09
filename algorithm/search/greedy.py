import sys

import networkx as nx

from algorithm.community.detection import louvain
from utils.counter import count_resistance
from utils.decoration import timer
from utils.graph_IO import read_gml
from utils.counter import count_position_entropy


class Greedy(object):
    def __init__(self, graph, func=louvain, func_args=dict()):
        self.graph = graph
        self.func = func
        self.func_args = func_args
        self.available_edges = None

    @timer(switch=True)
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
        print("You get %d edges available." % (len(self.available_edges)))

    @timer(switch=True)
    def anonymize(self, sum_of_edge=None, added_edges=None, interval=1):
        assert isinstance(sum_of_edge, int) or isinstance(added_edges, list)
        modules = self.func(self.graph, **self.func_args)
        self.get_available_edges(modules)
        resistance = count_resistance(self.graph, modules)
        print("Before anonymizing, the resistance of graph: %f" % resistance)

        if not sum_of_edge:
            self.graph.add_edges(added_edges)
        else:

            while sum_of_edge:  # adding sum_of_edge edges to make the graph anonymized
                add_edge = None
                min_resistance = sys.maxsize

                for edge in self.available_edges:
                    self.graph.add_edge(*edge)
                    resistance = count_resistance(self.graph, modules)

                    if resistance < min_resistance:
                        min_resistance = resistance
                        add_edge = edge

                    self.graph.remove_edge(*edge)

                self.available_edges.remove(add_edge)
                self.graph.add_edge(*add_edge)

                print(min_resistance)

                sum_of_edge -= 1

        modules = self.func(self.graph, **self.func_args)
        min_resistance = count_resistance(self.graph, modules)
        print("After anonymization, the resistance of graph is: %f" % min_resistance)


if __name__ == '__main__':
    from algorithm.community.detection import louvain, fast_newman
    temp_graph = read_gml("../../samples/dolphins.gml")
    greedy = Greedy(temp_graph)
    temp_modules = fast_newman(temp_graph, 11)

    greedy.anonymize(40, interval=1)
