import sys

import networkx as nx
import logging.config
from algorithm.community.detection import louvain
from algorithm.similarity.similarity import count_Jaccard_index
from utils.counter import count_security_index
from utils.decoration import timer
from simple_settings import settings
from utils.graph_IO import read

logger = logging.getLogger(settings.LOGGER_NAME)

class Greedy(object):
    def __init__(self, graph, sum_of_edge=None, added_edges=None, func=louvain, func_args=dict()):
        logger.info("Greedy start.")
        self.graph = read(graph)
        self.func = func
        self.func_args = func_args
        self.available_edges = None
        self.sum_of_edge = sum_of_edge
        self.added_edges = added_edges

    @timer(switch=settings.SWITCH)
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
        logger.info("Got %d edges available." % (len(self.available_edges)))

    @timer(switch=settings.SWITCH)
    def anonymize(self):
        sum_of_edge = self.sum_of_edge
        added_edges = self.added_edges

        assert isinstance(sum_of_edge, int) or isinstance(added_edges, list)
        pre_modules = self.func(self.graph, **self.func_args)
        self.get_available_edges(pre_modules)
        previous_security_index = count_security_index(self.graph, pre_modules)
        logger.info("Previous security index: %f" % previous_security_index)

        if not sum_of_edge:
            self.graph.add_edges(added_edges)
        else:
            count = 0
            while sum_of_edge:  # adding sum_of_edge edges to make the graph anonymized
                add_edge = None
                min_security_index = sys.maxsize

                for edge in self.available_edges:
                    self.graph.add_edge(*edge)
                    security_index = count_security_index(self.graph, pre_modules)

                    if security_index < min_security_index:
                        min_security_index = security_index
                        add_edge = edge

                    self.graph.remove_edge(*edge)

                self.available_edges.remove(add_edge)
                self.graph.add_edge(*add_edge)
                count += 1
                logger.info("%4d edge   security_index: %f" % (count, min_security_index))

                sum_of_edge -= 1
                # print(min_security_index)

        fin_modules = self.func(self.graph, **self.func_args)
        # finally_security_index = count_security_index(self.graph, fin_modules)
        logger.info("Jaccard_index: %f" % count_Jaccard_index(fin_modules, pre_modules))
        # print("After anonymizing, the moduels' similarity is: %f" % count_Jaccard_index(fin_modules, pre_modules))
        logger.info("Greedy ended.")

#
# if __name__ == '__main__':
#     from algorithm.community.detection import fast_newman
#     from utils.graph_IO import read_gml
#
#     temp_graph = read_gml("../../samples/dolphins.gml")
#     greedy = Greedy(temp_graph, func=fast_newman, func_args={"part_sum": 9})
#     greedy.anonymize(50)
