# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler
import time
from cfg import Cfg


def init_logger():
    # set logger
    logger = logging.getLogger("QPCR_LOGGER")

    log_file = "log/qpcr_"+time.strftime(u'%Y%m%d', time.localtime(time.time()))+".log"

    log_format = "%(asctime)s.%(msecs)03d - %(levelname)s -: %(message)s"
    data_format = '%Y-%m-%d %H:%M:%S'

    logger.setLevel('DEBUG')
    formatter = logging.Formatter(log_format, data_format)

    # output to console
    cmd_handler = logging.StreamHandler()
    cmd_handler.setFormatter(formatter)
    # cmd_handler.setLevel('INFO')      # set level

    # output to file
    # file_handler = TimedRotatingFileHandler(filename="log/qpcr", when="D", interval=1, backupCount=30)
    file_handler = TimedRotatingFileHandler(filename="log/qpcr", when="D", interval=1,
                                            backupCount=Cfg.LOG_DAY_BACKUP_COUNT, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(cmd_handler)
    logger.addHandler(file_handler)


if __name__ == '__main__':
    init_logger()
    logger = logging.getLogger("QPCR_LOGGER")

    while True:
        logger.debug(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        time.sleep(3)
