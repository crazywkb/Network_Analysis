# coding=utf-8
import logging.config
import os

from simple_settings import settings


def initial(logger_name="test"):
    os.environ['SIMPLE_SETTINGS'] = 'settings.' + os.sys.argv[1]
    settings.setup()
    logging.config.dictConfig(settings.LOGGING_CONFIG)
    return logging.getLogger(logger_name)


if __name__ == '__main__':
    logger = initial()
    logger.info("This is not a test.")
