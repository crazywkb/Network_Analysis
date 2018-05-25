import sys

import networkx as nx
import logging.config
from algorithm.community.detection import louvain
from algorithm.similarity.similarity import count_Jaccard_index
from utils.counter import count_security_index
from simple_settings import settings
from utils.graph_IO import read

logging.config.dictConfig(settings.LOGGING_CONFIG)
log = logging.getLogger('test')

class Greedy(object):
    def __init__(self, graph, sum_of_edge=None, added_edges=None, func=louvain, func_args=dict()):
        #log.info("Greedy start.")
        self.graph = read(graph)
        self.func = func
        self.func_args = func_args
        self.available_edges = None
        self.sum_of_edge = sum_of_edge
        self.added_edges = added_edges
        self.result_dict = dict()

        self.result_dict['graph'] = graph
        self.result_dict['func'] = func.__name__
        self.result_dict['func_args'] = func_args
        self.result_dict['edge_sum'] = sum_of_edge
        self.result_dict['added_edges'] = list()
        self.result_dict['security_index'] = list()
        self.result_dict['Jaccard_index'] = list()
        self.result_dict['pre_modules'] = None
        self.result_dict['fin_modules'] = None

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
        #log.info("Got %d edges available." % (len(self.available_edges)))

    def anonymize(self):

        sum_of_edge = self.sum_of_edge
        added_edges = self.added_edges

        assert isinstance(sum_of_edge, int) or isinstance(added_edges, list)
        pre_modules = self.func(self.graph, **self.func_args)
        self.result_dict['pre_modules'] = pre_modules.copy()

        self.get_available_edges(pre_modules)
        previous_security_index = count_security_index(self.graph, pre_modules)
        #log.info("Previous security index: %f" % previous_security_index)

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
                self.result_dict['added_edges'].append(add_edge)
                self.result_dict['security_index'].append(min_security_index)

                temp_modules = self.func(self.graph, **self.func_args)
                Jaccard_index = count_Jaccard_index(temp_modules, pre_modules)
                self.result_dict['Jaccard_index'].append(Jaccard_index)

                count += 1
                #log.info("%4d edge   security_index: %f" % (count, min_security_index))
                sum_of_edge -= 1

        fin_modules = self.func(self.graph, **self.func_args)
        self.result_dict['fin_modules'] = fin_modules.copy()
        log.info("Greedy %s %s %s %s" % (
        self.result_dict['graph'], self.result_dict['func'], self.result_dict['edge_sum'],
        self.result_dict['Jaccard_index']))
        return self.result_dict

        # finally_security_index = count_security_index(self.graph, fin_modules)
        #log.info("Jaccard_index: %f" % count_Jaccard_index(fin_modules, pre_modules))
        # print("After anonymizing, the moduels' similarity is: %f" % count_Jaccard_index(fin_modules, pre_modules))
        #log.info("Greedy ended.")
