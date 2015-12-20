# -*- coding: utf-8 -*-

import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    formatters={
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
    },
    loggers={
        'root': {'handlers': ['h'],
                 'level': logging.DEBUG}
    }
)


def config_logging():
    dictConfig(logging_config)
