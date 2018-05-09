from networkx import read_gml, write_gml


def read(path, label='label', destringizer=None):
    graph = read_gml(path, label=label, destringizer=destringizer)
    return graph


def write(graph, path, stringizer=None):
    write_gml(graph, path, stringizer=stringizer)


if __name__ == '__main__':
    pass
    # test_graph = read("../samples/football.gml")
    # from utils.count_entropy import count_two_dimension, count_one_dimension
    # from algorithm.community.community_detection import louvain, fast_newman
    # count_one_dimension(test_graph)
    # count_two_dimension(test_graph, louvain(test_graph))
    # count_two_dimension(test_graph, fast_newman(test_graph, 10))

