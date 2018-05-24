# coding=utf-8
import datetime
import logging.config
import os
import pickle
from collections import defaultdict

from simple_settings import settings

if __name__ == '__main__':
    os.environ['SIMPLE_SETTINGS'] = 'settings.master'
    settings.setup()
    from algorithm.search.ga import GA
    from algorithm.search.greedy import Greedy

    logging.config.dictConfig(settings.LOGGING_CONFIG)

    greedy_result = defaultdict(defaultdict)
    ga_result = defaultdict(defaultdict)

    for graph, sum_of_edge in settings.GRAPHS:
        for func, func_args in settings.FUNCS:
            greedy = Greedy(graph=graph, sum_of_edge=sum_of_edge, func=func, func_args=func_args)
            greedy.anonymize()
            greedy_result[graph][func.__name__] = greedy.result_dict

            for edges_sum in range(10, sum_of_edge + 1, 10):
                ga = GA(graph=graph, population_size=500, chromosome_size=edges_sum, func=func, func_args=func_args,
                        mate_probability=0.8, mutate_probability=0.02, disaster_interval=20, generation_num=200)
                ga.run()
                ga_result[graph][func.__name__] = ga.result_dict

    with open('greedy.result', 'wb') as f:
        pickle.dump(greedy_result, f)

    with open('ga.result', 'wb') as f:
        pickle.dump(ga_result, f)
    # ga = GA(**settings.GA_SETTINGS)
    # ga.run()
