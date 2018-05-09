from math import log

printed = False


def deco_print(is_print):
    """
    decoration of function
    :param is_print: print the result of func or not
    :return: func()
    """

    def deco(func):
        def __deco(*args, **kwargs):
            result = func(*args, **kwargs)

            if is_print:
                print("==========================================================================")
                print("Function %s output: %f." % (func.__name__, result))
                print()

            return result

        return __deco

    return deco


@deco_print(printed)
def count_position_entropy(graph):
    """
    count position entropy of graph
    :param graph: networkx.classes.graph.Graph
    :return: float, position entropy
    """
    total_degree = 2 * graph.number_of_edges()
    position_entropy = 0

    for node, node_degree in graph.degree:
        var = node_degree / total_degree
        position_entropy -= var * log(var, 2)

    return position_entropy


@deco_print(printed)
def count_structure_entropy(graph, modules):
    """
    count structure entropy of graph with modules.
    :param graph: networkx.classes.graph.Graph
    :param modules: dict, dict of modules, format: (key, value): (module_num, module_set)
    :return: float, structure entropy of graph
    """
    total_degree = 2 * graph.number_of_edges()
    assert total_degree != 0

    # first part: count information of nodes in its own module
    # second part: count information of the module that is accessible from random walk from nodes outside the module
    first_part, second_part = 0, 0

    for module in modules.values():
        module_volume = count_volume(graph, module)
        module_position_entorpy = 0
        module_total_degree = 0

        module_graph = graph.subgraph(module)
        module_graph_degree = 0

        for node in module:
            node_degree = graph.degree[node]
            var = node_degree / module_volume
            module_position_entorpy += var * log(var, 2)

            module_total_degree += node_degree
            module_graph_degree += module_graph.degree[node]

        cross_edges_sum = module_total_degree - module_graph_degree

        first_part -= (module_volume / total_degree) * module_position_entorpy
        second_part -= cross_edges_sum / total_degree * log(module_volume / total_degree, 2)

    structure_entropy = first_part + second_part
    return structure_entropy


@deco_print(printed)
def count_multiple_dimension(graph, modules_dict):
    """
    There may be a problem.
    :param graph: networkx.classes.graph.Graph
    :param modules_dict: dict, dict of moudles
    :return:
    """
    pass


@deco_print(printed)
def count_normalize_structure_entropy(graph, modules):
    structure_entropy = count_structure_entropy(graph, modules)
    position_entropy = count_position_entropy(graph)
    resistance = position_entropy - structure_entropy

    security_index = resistance / position_entropy
    normalized_structure_entropy = 1 - security_index
    return normalized_structure_entropy


@deco_print(printed)
def count_resistance(graph, modules):
    """
    count the resistance with modules
    :param graph: networkx.classes.graph.Graph
    :param modules: dict, dict of module
    :return: float, resistance of graph with modules
    """
    total_degree = 2 * graph.number_of_edges()
    resistance = 0

    for module in modules.values():
        module_volume = count_volume(graph, module)
        module_total_degree = 0
        module_graph = graph.subgraph(module)
        module_graph_degree = 0

        for node in module:
            module_total_degree += graph.degree[node]
            module_graph_degree += module_graph.degree[node]

        cross_edges_sum = module_total_degree - module_graph_degree
        resistance -= (module_volume - cross_edges_sum) / total_degree * log(module_volume / total_degree, 2)

    return resistance


def count_volume(graph, module):
    """
    count the volume of module in the graph
    :param graph: networkx.classes.graph.Graph
    :param module: list of node num
    :return: int, volume
    """
    return sum([graph.degree[node] for node in module])


if __name__ == '__main__':
    pass
    # import networkx as nx
    # from algorithm.community.community_detection import louvain, fast_newman
    # temp_graph = nx.karate_club_graph()
    # temp_modules = {0: {0, 2, 3, 7, 11, 12, 13}, 1: {1, 17, 19, 21}, 2: {4, 5, 6, 10, 16},
    #                 3: {8, 14, 15, 18, 20, 22, 30, 32},
    #                 4: {9, 23, 26, 27, 29, 33}, 5: {24, 25, 28, 31}}
    # temp_modules = {0:set(temp_graph.nodes)}
    # h1 = count_position_entropy(temp_graph)
    # h2 = count_structure_entropy(temp_graph, temp_modules)
    # resistance = count_resistance(temp_graph, temp_modules)
