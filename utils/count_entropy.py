from math import log


def count_one_dimension(graph, printed=True):
    """
    count graph's entropy of one dimension
    :param printed: boolean, print the result or not
    :param graph: networkx.classes.graph.Graph
    :return: structure entropy of one dimension
    """
    total_degree = 2 * len(graph.edges)
    entropy = 0

    for node, node_degree in graph.degree:
        temp = node_degree / total_degree
        entropy -= temp * log(temp, 2)

    if printed:
        print("=========================================================================================================")
        print("The one-dimensional structure entropy of graph %s: %f"%(graph, entropy))
        print()

    return entropy


def count_two_dimension(graph, modules_dict, printed=True):
    """
    count two-dimensional structure entropy
    :param printed: boolean, print the result or not
    :param graph: networkx.classes.graph.Graph
    :param modules_dict: dict of parts, (key, value): (module_num, modules_set)
    :return: structure entropy of two dimension
    """
    total_degree = len(graph.edges)
    assert total_degree != 0

    # first part: count information of nodes in its own module
    # second part: count information of the module that is accessible from random walk from nodes outside the module
    first_part = 0
    second_part = 0

    for module in modules_dict.values():
        module_capacity = len(module)
        module_entropy = 0
        sub_module_graph = graph.subgraph(module)
        module_degree = 0  # the sum of nodes' degree in module
        sub_module_degree = 0  # the sum of nodes' degree in sub_module

        for node in module:
            node_degree = graph.degree[node]
            temp = node_degree / module_capacity
            module_entropy += temp * log(temp, 2)

            module_degree += node_degree
            sub_module_degree += sub_module_graph.degree[node]

        cross_edges_sum = module_degree - sub_module_degree

        first_part -= (module_capacity / total_degree) * module_entropy
        second_part -= cross_edges_sum / total_degree * log(module_capacity / total_degree, 2)

    entropy = first_part + second_part
    if printed:
        print("=========================================================================================================")
        print("The two-dimensional structure entropy of graph %s: %f"%(graph, entropy))
        print("The modules' dict: ")
        for module_num, module in modules_dict.items():
            print("%-4s"%module_num, module)
        print()

    return entropy


def count_multiple_dimension(graph, modules_dict, printed=True):
    """
    There may be a problem.
    :param graph:
    :param modules_dict:
    :return:
    """
    # TODO: count multiple dimension structure entropy.
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
    from algorithm.community.community_detection import louvain, fast_newman
    import networkx as nx

    test_graph = nx.karate_club_graph()
    result_dict = fast_newman(test_graph, 4)
    (count_one_dimension(test_graph))
    (count_two_dimension(test_graph, result_dict))
