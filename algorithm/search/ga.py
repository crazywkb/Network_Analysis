import networkx as nx
import sys
import operator
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

        assert not self.population_size % 2

        self.pre_modules = None
        self.fin_modules = None
        self.available_edges = None

        self.populations = None
        self.security_index_list = None
        self.fitness_list = None

        self.global_best_security_index = sys.maxsize
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

    @timer(False)
    def generate_population(self):
        self.__get_available_edges()

        assert self.population_size <= comb(len(self.available_edges), self.chromosome_size)

        self.populations = list()

        for i in range(self.population_size):
            chromosome = list()
            now_length = 0

            while now_length < self.chromosome_size:
                gene = self.available_edges[randint(0, len(self.available_edges) - 1)]
                if gene in chromosome:
                    continue
                chromosome.append(gene)
                now_length += 1

            self.populations.append(chromosome)

    def __count_value(self):
        self.security_index_list = list()

        for chromosome in self.populations:
            self.graph.add_edges_from(chromosome)
            self.security_index_list.append(count_security_index(self.graph, self.pre_modules))
            self.graph.remove_edges_from(chromosome)

        posi, security_index = min(enumerate(self.security_index_list), key=operator.itemgetter(1))
        if security_index < self.global_best_security_index:
            self.global_best_chromosome = self.populations[posi]
            self.global_best_security_index = security_index

    @timer(False)
    def count_fitness(self):
        self.__count_value()
        self.fitness_list = list()
        fitness_sum = 0

        for security_index in self.security_index_list:
            fitness_sum += 1 / security_index
            self.fitness_list.append(fitness_sum)

        self.fitness_list = list(map(lambda x: x / fitness_sum, self.fitness_list))

    def __choose_chromosome(self):
        choose_fitness = random()
        choose_index = None

        for choose_index in range(len(self.populations)):
            if self.fitness_list[choose_index] > choose_fitness:
                break

        return self.populations[choose_index].copy()

    @timer(False)
    def select(self):
        new_populations = list()

        while len(new_populations) < self.population_size:
            a_chromosome = self.__choose_chromosome()
            b_chromosome = self.__choose_chromosome()

            self.__mate(a_chromosome, b_chromosome)
            self.__mutate(a_chromosome)
            self.__mutate(b_chromosome)

            new_populations.append(a_chromosome)
            new_populations.append(b_chromosome)

        self.populations = new_populations

    @timer(False)
    def __mate(self, a_chromosome, b_chromosome):
        if random() < self.mate_probability:
            mate_size = randint(0, self.chromosome_size)

            a_b = set(a_chromosome) - set(b_chromosome)
            b_a = set(b_chromosome) - set(a_chromosome)

            for mate_index in range(mate_size):
                b_a.add(a_chromosome.pop(randint(0, len(a_chromosome) - 1)))
                a_b.add(b_chromosome.pop(randint(0, len(b_chromosome) - 1)))

            a_b = list(a_b)
            b_a = list(b_a)

            for mate_index in range(mate_size):
                a_chromosome.append(b_a.pop(randint(0, len(b_a) - 1)))
                b_chromosome.append(a_b.pop(randint(0, len(a_b) - 1)))

    @timer(False)
    def __mutate(self, chromosome):
        for index in range(self.chromosome_size):
            if random() < self.mutate_probability:
                while True:
                    gene = self.available_edges[randint(0, len(self.available_edges) - 1)]
                    if gene not in chromosome:
                        chromosome[index] = gene
                        break

    @timer(False)
    def disaster(self):
        try:
            while True:
                self.populations.remove(self.global_best_chromosome)
        except ValueError:
            print("Disaster.")
            self.count_fitness()

    @timer(False)
    def run(self):
        self.generate_population()
        n = 0
        previous_best = 0

        while self.generation_num:
            self.count_fitness()
            print(self.global_best_security_index)

            if self.global_best_security_index == previous_best:
                n += 1
            else:
                n = 0
                previous_best = self.global_best_security_index

            if n == 20:
                self.disaster()
                n = 0
                self.count_fitness()

            self.select()
            self.generation_num -= 1

        self.graph.add_edges_from(self.global_best_chromosome)
        self.fin_modules = self.func(self.graph)
        print(count_Jaccard_index(self.pre_modules, self.fin_modules))


if __name__ == '__main__':
    ga = GA(graph='../../samples/dolphins.gml', func_args={'randomize': True}, func=louvain, population_size=100,
            chromosome_size=50, mate_probability=0.5, mutate_probability=0.05, generation_num=200)
    ga.run()

    # temp_graph = read('../../samples/dolphins.gml')
    # print(louvain(temp_graph))
