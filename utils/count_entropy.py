from math import log

import networkx as nx


def count_one_dimension(graph):
    """
    count graph's entropy of one dimension
    :param graph: networkx.classes.graph.Graph
    :return: entropy of one dimension
    """
    total_degree = 2 * len(graph.edges)
    entropy = 0

    for node, node_degree in graph.degree:
        temp = node_degree / total_degree
        entropy += temp * log(temp, 2)

    return entropy


def count_two_dimension(graph, part_list):
    pass


def count_multiple_dimension(graph, parts_list):
    """
    There may be a problem.
    :param graph:
    :param parts_list:
    :return:
    """
    pass


if __name__ == '__main__':
    test_graph = nx.karate_club_graph()
    print(count_one_dimension(test_graph))
