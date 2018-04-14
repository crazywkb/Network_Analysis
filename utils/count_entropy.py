from math import log

from algorithm.community.community_detection import louvain
import networkx as nx


def count_one_dimension(graph):
    """
    count graph's entropy of one dimension
    :param graph: networkx.classes.graph.Graph
    :return: structure entropy of one dimension
    """
    total_degree = 2 * len(graph.edges)
    entropy = 0

    for node, node_degree in graph.degree:
        temp = node_degree / total_degree
        entropy -= temp * log(temp, 2)

    return entropy


def count_two_dimension(graph, parts_dict):
    """

    :param graph: networkx.classes.graph.Graph
    :param parts_dict: dict of parts, (key, value): (part_num, part_list)
    :return: structure entropy of two dimension
    """
    total_degree = len(graph.edges)
    assert total_degree != 0

    # first part: count information of nodes in its own module
    # second part: count information of the module that is accessible from random walk from nodes outside the module
    first_part = 0
    second_part = 0

    for partition in parts_dict.values():
        part_capacity = len(partition)
        part_entropy = 0
        sub_graph = graph.subgraph(partition)
        partition_degree_global = 0
        partition_degree_sub = 0

        for node in partition:
            node_degree = graph.degree[node]
            temp = node_degree / part_capacity
            part_entropy += temp * log(temp, 2)

            partition_degree_global += node_degree
            partition_degree_sub += sub_graph.degree[node]

        cross_edges_sum = partition_degree_global - partition_degree_sub

        first_part -= (part_capacity / total_degree) * part_entropy
        second_part -= cross_edges_sum / total_degree * log(part_capacity / total_degree, 2)

    return first_part + second_part


def count_multiple_dimension(graph, parts_list):
    """
    There may be a problem.
    :param graph:
    :param parts_list:
    :return:
    """
    pass
    return 0


def count_volume(graph, module):
    """
    count the volume of module in the graph
    :param graph: networkx.classes.graph.Graph
    :param module: list of node num
    :return: int, volume
    """
    return sum([graph.degree[node] for node in module])


if __name__ == '__main__':
    test_graph = nx.karate_club_graph()
    print(count_one_dimension(test_graph))
    partition_dict = louvain(test_graph)
    print(count_two_dimension(test_graph, partition_dict))