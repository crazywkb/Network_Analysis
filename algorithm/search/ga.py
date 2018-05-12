import networkx as nx
import sys
import logging.config
from utils.graph_IO import read
from scipy.special import comb
from simple_settings import settings
from algorithm.similarity.similarity import count_Jaccard_index
from algorithm.community.detection import louvain
from utils.counter import count_security_index
from utils.decoration import timer
from random import randint, random


# log = logging.getLogger(settings.LOGGER_NAME)

class GA(object):
    def __init__(self, **kwargs):
        self.graph = read(kwargs['graph'])
        self.population_size = kwargs['population_size']
        self.chromosome_size = kwargs['chromosome_size']
        self.mate_probability = kwargs['mate_probability']
        self.mutate_probability = kwargs['mutate_probability']
        self.generation_num = kwargs['generation_num']
        self.func = kwargs['func']
        self.func_args = kwargs['func_args']

        self.pre_modules = None
        self.fin_modules = None
        self.available_edges = None

        self.populations = None

        self.global_best_similarity = sys.maxsize
        self.global_best_chromosome = None

    def __set_pre_modules(self):
        self.pre_modules = self.func(self.graph, **self.func_args)

    def __get_available_edges(self):
        self.__set_pre_modules()
        inside_edges = set()

        for module in self.pre_modules.values():
            sub_graph = nx.complete_graph(module)
            inside_edges.update(sub_graph.edges)

        module_cross_edges = nx.complete_graph(self.graph.nodes).edges - inside_edges
        self.available_edges = list(module_cross_edges - self.graph.edges)

    @timer(True)
    def generate_population(self):
        self.__get_available_edges()

        assert self.population_size <= comb(len(self.available_edges), self.chromosome_size)

        self.populations = list()

        for i in range(self.population_size):
            chromosome = list()
            now_length = 0

            while now_length < self.chromosome_size:
                gene = self.available_edges[randint(0, len(self.available_edges) - 1)]
                if gene in

    def __count_value(self):
        pass

    @timer(True)
    def count_fitness(self):
        self.__count_value()
        pass

    @timer(True)
    def select(self):
        pass

    @timer(True)
    def mate(self):
        self.__random_mix(1, 2)
        pass

    def __random_mix(self, a_chromosome, b_chromosome):
        pass

    @timer(True)
    def mutate(self):
        pass

    @timer(True)
    def disaster(self):
        pass

    @timer(True)
    def run(self):
        # log.info("start")
        self.generate_population()

        while self.generation_num:
            self.count_fitness()
            self.select()
            self.mate()
            self.mutate()
            self.disaster()

            self.generation_num -= 1

        # log.info("end")


if __name__ == '__main__':
    ga = GA(graph='../../samples/dolphins.gml', func_args=dict(), func=louvain, population_size=100, chromosome_size=30,
            mate_probability=0.6, mutate_probability=0.02, generation_num=100)
    ga.run()
    # temp_graph = read('../../samples/dolphins.gml')
    # print(louvain(temp_graph))
