from community.community_louvain import best_partition
from networkx.algorithms.community import girvan_newman


def louvain(graph):
    best_partition(graph)
    pass


def fast_newman(graph, part_sum):
    girvan_newman(graph, part_sum)
    pass


if __name__ == '__main__':
    pass
