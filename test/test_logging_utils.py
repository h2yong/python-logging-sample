import logging

import allure

from app import logging_utils

@allure.story("基础功能")
def test_logging_utils():
    logger = logging_utils.get_logger(channel="test")
    logger.info("this is info.")


@allure.story("重置logger.handlers")
def test_logging_utils_with_handlers():
    log = logging.getLogger("app")
    stream_handler = logging.StreamHandler()
    log.addHandler(stream_handler)
    log.setLevel("info".upper())
    logger = logging_utils.get_logger(logger=log, channel="test")
    logger.warning("this is warning.")
