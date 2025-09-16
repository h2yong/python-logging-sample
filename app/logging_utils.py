import json
import logging

from typing import Any


def get_logger(logger: Any = None,
               name: str = "base",
               logger_type: str = "pa_access",
               channel: Any = None,
               level: str = "info") -> Any:
    """获取logger.

    :param logger: logger
    :param name: logger name
    :param logger_type: logger type
    :param channel: logger channel
    :param level: logger level
    :return: logger
    """
    if logger:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
        logger.propagate = True
    else:
        logger = logging.getLogger(name)
    specs = {
        'type': logger_type,
        'date': "%(asctime)s",
        'level': "%(levelname)s",
        'channel': channel,
        'message': "%(message)s"
    }

    logging.Formatter.default_msec_format = '%s.%03d+0800'
    logging.Formatter.default_time_format = '%Y-%m-%dT%H:%M:%S'
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(json.dumps(specs)))
    logger.addHandler(stream_handler)
    logger.setLevel(level.upper())
    return logger
