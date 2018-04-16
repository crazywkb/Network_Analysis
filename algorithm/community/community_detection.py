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
    :return: dict, the result of partition, {module_num: {module}}
    """
    partition_result = best_partition(graph, partition=partition, randomize=randomize)
    partition_dict_keys = set(partition_result.values())
    partition_dict = defaultdict(set)
    partition_dict.fromkeys(list(partition_dict_keys))

    for node, part_num in partition_result.items():
        partition_dict[part_num].add(node)

    return partition_dict


def fast_newman(graph, part_sum):
    """
    wrap girvan_newman, adding part_sum to limit the partitions
    :param graph: networkx.classes.graph.Graph
    :param part_sum: int
    :return: dict, same with louvain()
    """
    partitions_iter = girvan_newman(graph)
    result = next(partitions_iter)
    for result in range(part_sum - 2):
        result = next(partitions_iter)

    partition_dict = defaultdict(set)
    partition_dict.fromkeys(range(part_sum))

    for module_num, module in enumerate(result):
        partition_dict[module_num].update(module)

    return partition_dict


if __name__ == '__main__':
    pass
