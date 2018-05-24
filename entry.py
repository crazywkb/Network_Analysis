# coding=utf-8
import datetime
import logging.config
import os

from simple_settings import settings

if __name__ == '__main__':
    os.environ['SIMPLE_SETTINGS'] = 'settings.master'
    settings.setup()
    from algorithm.search.ga import GA
    from algorithm.search.greedy import Greedy

    logging.config.dictConfig(settings.LOGGING_CONFIG)
    # greedy = Greedy(**settings.GREEDY_SETTINGS)
    # greedy.anonymize()

    ga = GA(**settings.GA_SETTINGS)
    ga.run()
