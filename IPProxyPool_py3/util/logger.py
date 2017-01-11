# coding:utf-8
import logging

__author__ = 'qiye'

logger = logging.getLogger()


def logger_proxy(proxy):
    logger.setLevel(logging.INFO)
    logger.info(proxy)
