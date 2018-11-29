# 
# Copyright 2018 Kionix Inc.
#
import logging
from logging import INFO, DEBUG, WARNING, ERROR  # pylint: disable=unused-import


def get_logger(name):
    logging.basicConfig(format='%(asctime)s %(levelname)s :\t%(filename)s (%(lineno)d) :\t%(funcName)s :\t%(message)s')
    logger = logging.getLogger(name)
    return logger
