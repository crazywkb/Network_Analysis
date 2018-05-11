from utils.decoration import watcher

switch = False


@watcher(switch=switch)
def count_common_parts_num(modules_a, modules_b):
    """
    count the number of pairs simultaneously joined together
    :param modules_a: dict
    :param modules_b: dict
    :return: float
    """
    result = 0

    for a_module in modules_a.values():
        for b_module in modules_b.values():
            intersection_length = len(a_module.intersection(b_module))
            if intersection_length > 1:
                result += intersection_length * (intersection_length - 1) / 2
    return result


@watcher(switch=switch)
def count_combinations(module=None, modules=None):
    """
    count combinations of module or modules
    :param module: set
    :param modules: dict
    :return: float
    """
    assert isinstance(module, set) or isinstance(modules, dict)
    result = 0

    if module:
        length = len(module)
        result = length * (length - 1) / 2
    else:
        for module in modules.values():
            length = len(module)
            result += length * (length - 1) / 2

    return result


@watcher(switch=switch)
def count_Jaccard_index(modules_a, modules_b):
    """
    count Jaccard index of modules_a and modules_b
    :param modules_a: dict
    :param modules_b: dict
    :return: float
    """
    r = count_common_parts_num(modules_a, modules_b)
    u_v_2r = count_combinations(modules=modules_a) + count_combinations(modules=modules_b)

    print(r, u_v_2r)
    return r / (u_v_2r - r)


if __name__ == '__main__':
    pass
    # import networkx as nx
    #
    # graph = nx.karate_club_graph()
    #
    # a_modules = {0: {0, 1, 2, 3, 7, 9, 11, 12, 13, 17, 19, 21}, 1: {4, 5, 6, 10, 16},
    #              2: {8, 14, 15, 18, 20, 22, 23, 26, 27, 29, 30, 32, 33}, 3: {24, 25, 28, 31}}
    # b_modules = {0: {0, 1, 3, 7, 12, 13, 17, 19, 21}, 1: {2, 24, 25, 27, 28, 31}, 2: {4, 5, 6, 10, 16},
    #              3: {32, 33, 8, 14, 15, 18, 20, 22, 23, 26, 29, 30}, 4: {9}, 5: {11}}
    #
    # # print(count_semblance(a_modules, b_modules))
    # # The result should be: 118.0, 287.0 and 0.6982248520710059
    # print(count_Jaccard_index(a_modules, b_modules))
