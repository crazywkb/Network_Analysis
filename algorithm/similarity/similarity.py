def count_semblance(partition_a, partition_b):
    print(len(partition_b), len(partition_a))
    u_v_2r = 0
    r = 0

    for part in partition_a.values():
        length = len(part)
        u_v_2r += length * (length - 1) / 2
        for i in range(0, len(part) - 1):
            node_a = part[i]
            for j in range(i + 1, len(part)):
                node_b = part[j]

                sub_set = set()
                sub_set.update([node_a, node_b])
                for temp in partition_b.values():
                    if sub_set.issubset(temp):
                        r += 1
                        break
    for part in partition_b.values():
        u_v_2r += len(part) * (len(part) - 1) / 2
    return r / (u_v_2r - r)


def count_similarity(a_modules, b_modules):
    total_kinds = 0
    same_kinds = 0

    for a_module in a_modules.values():
        total_kinds += count_combinations(a_module)

        for a_node in a_module:
            for b_node in a_module:
                if a_node != b_node:
                    sub_set = set()
                    sub_set.update([a_node, b_node])
                    for b_module in b_modules.values():
                        if sub_set.issubset(b_module):
                            same_kinds += 1
                            break

    for b_module in b_modules.values():
        total_kinds += count_combinations(b_module)

    return same_kinds / (total_kinds - same_kinds)


def count_combinations(module):
    length = len(module)
    return length * (length - 1) / 2


if __name__ == '__main__':
    import networkx as nx

    graph = nx.karate_club_graph()
    from algorithm.community.detection import louvain, fast_newman

    a_modules = louvain(graph)
    b_modules = fast_newman(graph, 4)

    print(count_similarity(a_modules, b_modules))
