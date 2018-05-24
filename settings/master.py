from algorithm.community.detection import louvain, fast_newman

GRAPH_PATH = "samples/karate.gml"

GRAPHS = [('samples/karate.gml', 10), ('samples/dolphins.gml', 10)]

FUNCS = [(louvain, dict()), (fast_newman, {'part_sum': 5})]

PART_SUM = 5

SWITCH = False

GA_SETTINGS = {
    'graph': 'samples/dolphins.gml',
    'func': fast_newman,
    'func_args': {'part_sum': 5},
    'population_size': 200,
    'chromosome_size': 30,
    'mate_probability': 0.7,
    'mutate_probability': 0.02,
    'generation_num': 100,
    'disaster_interval': 20
}

GREEDY_SETTINGS = {
    'graph': 'samples/dolphins.gml',
    'added_edges': None,
    'sum_of_edge': 10,
    'func': louvain,
    'func_args': {},
}

LOGGER_NAME = 'test'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '[%(asctime)s] %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
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
