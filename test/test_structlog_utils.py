import os

import allure

from app import structlog_utils


@allure.story("基础功能")
def test_structlog_utils():
    logger = structlog_utils.get_logger(name=__name__)
    logger.info("info message")

    os.environ["ENV"] = "production"
    log = structlog_utils.get_logger(name=__name__)
    log.warning("warning message")
