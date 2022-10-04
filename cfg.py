# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger("QPCR_LOGGER")


class Cfg(object):
    try:
        LOG_DAY_BACKUP_COUNT = 365

    except Exception as err:
        logger.error(f"Config file Error: {err}")