from math import log

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
        entropy += temp * log(temp, 2)

    return entropy


def count_two_dimension(graph, parts_list):
    """

    :param graph: networkx.classes.graph.Graph
    :param parts_list: list
    :return: structure entropy of two dimension
    """
    parts_sum = len(parts_list)
    total_degree = len(graph.edges)

    # first part: count information of nodes in its own module
    # second part: count information of the module that is accessible from random walk from nodes outside the module
    first_part = 0
    second_part = 0
    for partition in parts_list:
        part_capacity = len(partition)
        part_entropy = 0

        for node in partition:
            node_degree = graph.degree[node]
            temp = node_degree / part_capacity
            part_entropy += temp * log(temp, 2)

        first_part -= (part_capacity / total_degree) * part_entropy

        sub_graph = graph.subgraph(partition)
        diff_edges = graph.edges - sub_graph.edges
        diff_edges_sum = 0

        for src, des in diff_edges:
            if src in partition or des in partition:
                diff_edges += 1

        second_part += diff_edges_sum / total_degree * log(part_capacity)


    return first_part - second_part


def count_multiple_dimension(graph, parts_list):
    """
    There may be a problem.
    :param graph:
    :param parts_list:
    :return:
    """
    pass


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
