import networkx as nx
from algorithm.community.community_detection import louvain
from utils.count_entropy import count_resistance
from utils.graph_IO import read_gml
import sys
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
        print("You get %d edges available." % (len(self.available_edges)))

    def anonymize(self, sum_of_edge=None, added_edges=None, interval=1):
        assert isinstance(sum_of_edge, int) or isinstance(added_edges, list)
        modules = self.func(self.graph, **self.func_args)
        self.get_available_edges(modules)
        resistence = count_resistance(self.graph, modules)
        print("Before anonymizing, the resistence of graph: %f" % resistence)

        if not sum_of_edge:
            self.graph.add_edges(added_edges)
        else:

            while sum_of_edge:  # adding sum_of_edge edges to make the graph anonymized
                add_edge = None
                min_resistence = sys.maxsize

                for edge in self.available_edges:
                    self.graph.add_edge(*edge)
                    resistence = count_resistance(self.graph, modules)

                    if resistence < min_resistence:
                        min_resistence = resistence
                        add_edge = edge

                    self.graph.remove_edge(*edge)

                self.available_edges.remove(add_edge)
                self.graph.add_edge(*add_edge)

                if not sum_of_edge % interval:
                    modules = self.func(self.graph, **self.func_args)
                    min_resistence = count_resistance(self.graph, modules)
                    # self.get_available_edges(modules)
                    print("Adding %d edge per time, the resistence: %f"%(interval, min_resistence))

                sum_of_edge -= 1

        modules = self.func(self.graph, **self.func_args)
        min_resistence = count_resistance(self.graph, modules)
        print("After anonymization, the resistence of graph is: %f"%min_resistence)


if __name__ == '__main__':
    temp_graph = read_gml("../../samples/dolphins.gml")
    greedy = Greedy(temp_graph)
    temp_modules = louvain(temp_graph)

    start_time = time.time()
    greedy.anonymize(40, interval=40)
    end_time = time.time()

    print("Total cost: " + str(end_time - start_time))