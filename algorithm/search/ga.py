import logging.config
import operator
import sys
from random import randint, random

import networkx as nx
from scipy.special import comb
from simple_settings import settings

from algorithm.similarity.similarity import count_Jaccard_index
from utils.counter import count_security_index
from utils.graph_IO import read

logging.config.dictConfig(settings.LOGGING_CONFIG)
log = logging.getLogger('test')


class GA(object):
    def __init__(self, **kwargs):
        #log.info("GA Start.")
        self.graph = read(kwargs['graph'])
        self.population_size = kwargs['population_size']
        self.chromosome_size = kwargs['chromosome_size']
        self.mate_probability = kwargs['mate_probability']
        self.mutate_probability = kwargs['mutate_probability']
        self.generation_num = kwargs['generation_num']
        self.func = kwargs['func']
        self.func_args = kwargs['func_args']
        self.disaster_interval = kwargs['disaster_interval']

        assert not self.population_size % 2

        self.pre_modules = None
        self.fin_modules = None
        self.available_edges = None

        self.populations = None
        self.security_index_list = None
        self.fitness_list = None

        self.local_best_security_index = None
        self.local_best_chromosome = None
        self.global_best_security_index = sys.maxsize
        self.global_best_chromosome = None

        self.result_dict = dict()
        self.result_dict['graph'] = kwargs['graph']
        self.result_dict['func'] = kwargs['func'].__name__
        self.result_dict['func_args'] = kwargs['func_args']
        self.result_dict['edge_sum'] = kwargs['chromosome_size']
        self.result_dict['populations_size'] = kwargs['population_size']
        self.result_dict['mate_probability'] = kwargs['mate_probability']
        self.result_dict['mutate_probablity'] = kwargs['mutate_probability']
        self.result_dict['generation_num'] = kwargs['generation_num']
        self.result_dict['added_edges'] = list()
        self.result_dict['security_index'] = None
        self.result_dict['Jaccard_index'] = None
        self.result_dict['pre_modules'] = None
        self.result_dict['fin_modules'] = None

    def __set_pre_modules(self):
        self.pre_modules = self.func(self.graph, **self.func_args)
        self.result_dict['pre_modules'] = self.pre_modules.copy()

    def __get_available_edges(self):
        self.__set_pre_modules()
        inside_edges = set()

        for module in self.pre_modules.values():
            sub_graph = nx.complete_graph(module)
            inside_edges.update(sub_graph.edges)

        module_cross_edges = nx.complete_graph(self.graph.nodes).edges - inside_edges
        self.available_edges = list(module_cross_edges - self.graph.edges)
        #log.info("Got %d edges available." % (len(self.available_edges)))

    def __get_random_chromosome(self, num):
        for i in range(num):
            chromosome = list()
            now_length = 0

            while now_length < self.chromosome_size:
                gene = self.available_edges[randint(0, len(self.available_edges) - 1)]
                if gene in chromosome:
                    continue
                chromosome.append(gene)
                now_length += 1

            self.populations.append(chromosome)

    def generate_population(self):
        self.__get_available_edges()

        assert self.population_size <= comb(len(self.available_edges), self.chromosome_size)

        self.populations = list()
        self.__get_random_chromosome(self.population_size)

    def __count_value(self):
        self.security_index_list = list()

        for chromosome in self.populations:
            self.graph.add_edges_from(chromosome)
            self.security_index_list.append(count_security_index(self.graph, self.pre_modules))
            self.graph.remove_edges_from(chromosome)

        posi, self.local_best_security_index = min(enumerate(self.security_index_list), key=operator.itemgetter(1))
        self.local_best_chromosome = self.populations[posi]

        if self.local_best_security_index < self.global_best_security_index:
            self.global_best_chromosome = self.local_best_chromosome
            self.global_best_security_index = self.local_best_security_index

    def count_fitness(self):
        self.__count_value()
        self.fitness_list = list()
        fitness_sum = 0

        max_security = max(self.security_index_list)
        for security_index in self.security_index_list:
            fitness_sum += max_security - security_index
            self.fitness_list.append(fitness_sum)

        self.fitness_list = list(map(lambda x: x / fitness_sum, self.fitness_list))

    def __choose_chromosome(self):
        choose_fitness = random()
        choose_index = None

        for choose_index in range(len(self.populations)):
            if self.fitness_list[choose_index] > choose_fitness:
                break

        return self.populations[choose_index].copy()

    def sub_select(self):
        a_chromosome = self.__choose_chromosome()
        b_chromosome = self.__choose_chromosome()

        self.__mate(a_chromosome, b_chromosome)
        self.__mutate(a_chromosome)
        self.__mutate(b_chromosome)
        return [a_chromosome, b_chromosome]

    def select(self):
        new_populations = list()

        while len(new_populations) < self.population_size:
            new_populations.extend(self.sub_select())

        self.populations = new_populations

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

    def __mutate(self, chromosome):
        for index in range(self.chromosome_size):
            if random() < self.mutate_probability:
                while True:
                    gene = self.available_edges[randint(0, len(self.available_edges) - 1)]
                    if gene not in chromosome:
                        chromosome[index] = gene
                        break

    def disaster(self):
        count = self.populations.count(self.local_best_chromosome)
        self.populations = []
        self.__get_random_chromosome(self.population_size - len(self.populations))
        #log.info("Disaster: remove %4d chromosomes." % count)
        self.count_fitness()


    def save(self):
        nx.write_gml(self.graph, 'test.gml')

    def run(self):
        self.generate_population()
        n = 0
        previous_best = 0
        generation = 0
        while self.generation_num:
            self.count_fitness()
            if self.global_best_security_index == previous_best:
                n += 1
            else:
                n = 0
                previous_best = self.global_best_security_index

            if n == self.disaster_interval:
                self.disaster()
                n = 0
                self.count_fitness()
            generation += 1
            # log.info("Generation %4d, local_min_security_index: %.16f, global_min_security_index: %.16f." % (
            #    generation, self.local_best_security_index, self.global_best_security_index))
            self.select()
            self.generation_num -= 1

        self.graph.add_edges_from(self.global_best_chromosome)
        self.fin_modules = self.func(self.graph, **self.func_args)
        # print(count_Jaccard_index(self.pre_modules, self.fin_modules))
        jaccard_index = count_Jaccard_index(self.pre_modules, self.fin_modules)
        # log.info("Jaccard_index: %f" % jaccard_index)
        ##log.info("GA Ended.")

        self.result_dict['security_index'] = self.global_best_security_index
        self.result_dict['Jaccard_index'] = jaccard_index
        self.result_dict['added_edges'] = self.global_best_chromosome
        self.result_dict['fin_modules'] = self.fin_modules.copy()

        log.info("GA     %25s %15s %4d   %s" % (
        self.result_dict['graph'], self.result_dict['func'], self.result_dict['edge_sum'],
        self.result_dict['Jaccard_index']))

        return self.result_dict
