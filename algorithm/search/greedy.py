import networkx as nx
from algorithm.community.community_detection import louvain
from utils.count_entropy import count_resistance
from simple_settings import settings


class Greedy(object):
    def __init__(self, graph, func=louvain, func_args=dict()):
        self.graph = graph.copy()
        self.community_detection_func = func
        self.community_detection_func_args = func_args
        self.diff_edges = list()
        self.max_resistance = 0

    def __get_diff_edges(self, modules):
        full_edges = {(i, j) for i in range(self.graph.number_of_nodes()) for j in
                      range(i + 1, self.graph.number_of_nodes())}
        diff_edges = full_edges - self.graph.edges
        self.diff_edges = list()
        for edge in diff_edges:
            src, des = edge
            flag = False
            for module in modules.values():
                if src in module and des in module:
                    flag = True
                    break
            if not flag:
                self.diff_edges.append(edge)


    def anonymize(self, edges_sum=None, added_edges=None, intervals=1):
        assert isinstance(edges_sum, int) or isinstance(added_edges, list)
        modules = self.community_detection_func(self.graph, **self.community_detection_func_args)
        self.__get_diff_edges(modules)
        max_resistance = count_resistance(self.graph, modules)
        print("Bebore anonymize: the resistance of graph is: %f" % max_resistance)

        if not edges_sum:
            self.graph.add_edges(added_edges)
        else:
            count = 0

            while edges_sum:
                add_edge = None
                max_resistance = 1000

                for edge in self.diff_edges:
                    self.graph.add_edge(*edge)
                    temp_resistance = count_resistance(self.graph, modules)
                    if temp_resistance < max_resistance:
                        max_resistance = temp_resistance
                        add_edge = edge
                    self.graph.remove_edge(*edge)

                self.diff_edges.remove(add_edge)
                edges_sum -= 1
                self.graph.add_edge(*add_edge)
                count += 1

                if count == intervals:
                    modules = self.community_detection_func(self.graph, **self.community_detection_func_args)
                    max_resistance = count_resistance(self.graph, modules)
                    self.__get_diff_edges(modules)
                    print("Adding %d edge per time, resistance: %f"%(intervals, max_resistance))
                    count = 0

        modules = self.community_detection_func(self.graph, **self.community_detection_func_args)
        max_resistance = count_resistance(self.graph, modules)
        print("After anonymize: the resistance of graph is: %f"%max_resistance)


if __name__ == '__main__':
    import networkx as nx
    from utils.graph_IO import read_gml

    graph = read_gml("../../samples/dolphins.gml")
    nx.draw_networkx(graph)
    # test_graph = nx.karate_club_graph()
    # greedy = Greedy(test_graph, louvain)
    # greedy.anonymize(100, intervals=1)