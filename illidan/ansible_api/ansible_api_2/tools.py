#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import time
import json
import logging
import os
from . import __version__

__all__ = ['Tool']


class Tool(object):

    LOGGER = None

    @staticmethod
    def init_logger(path):
        log_formatter = "%(asctime)s | %(levelname)s - %(message)s"
        date_formatter = "%Y-%m-%d %H:%M:%S"
        if isinstance(path, str) and os.path.exists(os.path.dirname(path)):
            Tool.LOGGER = logging.getLogger('ansible-api-2.%s' % __version__)
            logHandler = logging.handlers.TimedRotatingFileHandler(path, when='midnight')
            logFormatter = logging.Formatter(fmt=log_formatter, datefmt=date_formatter)
            logHandler.setFormatter(logFormatter)
            Tool.LOGGER.addHandler(logHandler)
            Tool.LOGGER.setLevel(logging.DEBUG)
            Tool.LOGGER.propagate = False  # disable console output
        else:
            logging.basicConfig(level=logging.DEBUG,
                                format=log_formatter, datefmt=date_formatter)
            Tool.LOGGER = logging.getLogger('ansible-api-2.%s' % __version__)

    @staticmethod
    def getmd5(str):
        import hashlib
        m = hashlib.md5()
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def jsonal(data):
        return json.dumps(data)

    @staticmethod
    def parsejson(string):
        return json.loads(string.decode('utf-8'))
