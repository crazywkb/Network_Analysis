from networkx import read_gml, write_gml


def read(path, label='label', destringizer=None):
    graph = read_gml(path, label=label, destringizer=destringizer)
    return graph


def write(graph, path, stringizer=None):
    write_gml(graph, path, stringizer=stringizer)


if __name__ == '__main__':
    test_graph = read("../samples/football.gml")
    print(len(test_graph.edges))
