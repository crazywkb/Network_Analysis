from community.community_louvain import best_partition
from networkx.algorithms.community import girvan_newman
from collections import defaultdict


def louvain(graph, partition=None, randomize=False):
    partition_result = best_partition(graph, partition=partition, randomize=randomize)
    partition_dict_keys = set(partition_result.values())
    partition_dict = defaultdict(list)
    partition_dict.fromkeys(partition_dict_keys)

    for node, part_num in partition_result.items():
        partition_dict[part_num].append(node)

    return partition_dict


def fast_newman(graph, part_sum):
    girvan_newman(graph, part_sum)
    pass


if __name__ == '__main__':
    pass
