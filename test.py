# coding=utf-8
import logging.config
import os
import pickle
import sys
import multiprocessing
from collections import defaultdict

from simple_settings import settings

if __name__ == '__main__':
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    os.environ['SIMPLE_SETTINGS'] = 'settings.master'
    settings.setup()
    from algorithm.search.ga import GA
    from algorithm.search.greedy import Greedy

    logging.config.dictConfig(settings.LOGGING_CONFIG)

    logger = logging.getLogger('test')

    greedy_result = defaultdict(defaultdict)
    ga_result = defaultdict(defaultdict)

    result = {
        'greedy': greedy_result,
        'ga': ga_result
    }

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    processes = []
    for graph, sum_of_edge in settings.GRAPHS:
        for func, func_args in settings.FUNCS:
            greedy = Greedy(graph=graph, sum_of_edge=sum_of_edge, func=func, func_args=func_args)
            processes.append(
                (('greedy', graph, sum_of_edge, func.__name__, func_args), pool.apply_async(greedy.anonymize)))

            for edges_sum in range(1, sum_of_edge + 1, 1):
                ga = GA(graph=graph, population_size=400, chromosome_size=edges_sum, func=func, func_args=func_args,
                        mate_probability=0.8, mutate_probability=0.02, disaster_interval=20, generation_num=200)
                processes.append((('ga', graph, edges_sum, func.__name__, func_args), pool.apply_async(ga.run)))

    pool.close()
    pool.join()

    for info, process in processes:
        key, graph, sum_of_edge, func_name, func_args = info
        try:
            result[key][graph][func_name] = process.get()
        except:
            continue

    with open('result.dict', 'wb') as f:
        pickle.dump(result, f)
