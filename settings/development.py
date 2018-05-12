from algorithm.community.detection import louvain, fast_newman

SAMPLES_NETWORK_PATH = "samples"

SEARCH_TYPE = ('NORMAL', 'GREDDY', 'GA')

SEARCH_MODE = 'GREDDY'

# update the network until add the number of UPDATE_INTERVAL edges while counting structure entropy.
UPDATE_INTERVAL = 5

# list of the community detection algorithm
ALGORITHM_LIST = ["louvain", "fast_newman"]

GRAPH_PATH = "samples/karate.gml"

SWITCH = False

GA_SETTINGS = {
    'graph': 'samples/dolphins.gml',
    'func': louvain,
    'func_args': dict(),
    'population_size': 100,
    'chromosome_size': 30,
    'mate_probability': 0.8,
    'mutate_probability': 0.1,
    'generation_num': 100
}

LOGGER_NAME = 'test'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': 'logs/logging.log',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'test': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    }
}
