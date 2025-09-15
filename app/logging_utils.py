import json
import logging


def get_logger(logger=None, name="base", logger_type="pa_access", channel=None, level="info"):
    """
    获取logger

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
