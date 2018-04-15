from collections import defaultdict

from community.community_louvain import best_partition
from networkx.algorithms.community import girvan_newman


def louvain(graph, partition=None, randomize=False):
    """
    warp the best_partition, change the result into a dict
    Compute the partition of the graph nodes which maximises the modularity
    (or try..) using the Louvain heuristices

    :param graph: networkx.classes.graph.Graph
    :param partition: dict, optional.
    :param randomize: boolean, optional
    :return: dict, the result of partition, {module_num: [module]}
    """
    partition_result = best_partition(graph, partition=partition, randomize=randomize)
    partition_dict_keys = set(partition_result.values())
    partition_dict = defaultdict(list)
    partition_dict.fromkeys(list(partition_dict_keys))

    for node, part_num in partition_result.items():
        partition_dict[part_num].append(node)

    return partition_dict


def fast_newman(graph, part_sum):
    girvan_newman(graph)
    part_sum.test()
    pass


if __name__ == '__main__':
    pass
