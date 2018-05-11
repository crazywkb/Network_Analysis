# coding=utf-8
import os
from simple_settings import settings
import logging.config


def initial():
    os.environ['SIMPLE_SETTINGS'] = 'settings.' + os.sys.argv[1]
    settings.setup()
    logging.config.dictConfig(settings.LOGGING_CONFIG)


def get_logger(name):
    assert isinstance(name, str)
    return logging.getLogger(name)


if __name__ == '__main__':
    initial()
    logger = get_logger("test")
    logger.info("This is not a test.")
