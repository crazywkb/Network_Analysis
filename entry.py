# coding=utf-8
import datetime
import logging.config
import os

from simple_settings import settings

if __name__ == '__main__':
    os.environ['SIMPLE_SETTINGS'] = 'settings.development'
    settings.setup()
    from algorithm.search.ga import GA

    logging.config.dictConfig(settings.LOGGING_CONFIG)
    logger = logging.getLogger('test')
    logger.info("Program start: %s" % datetime.datetime.now().strftime("%Y:%m:%d"))
    ga = GA(**settings.GA_SETTINGS)
    ga.run()
    logger.info("Program end: %s" % datetime.datetime.now().strftime("%Y:%m:%d"))
