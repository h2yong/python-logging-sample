import os

import allure

from app import loguru_utils


@allure.story("基础功能")
def test_structlog_utils():
    logger = loguru_utils.get_logger()
    # logger.info("info message")

    os.environ["ENV"] = "production"
    log = loguru_utils.get_logger()
    log.warning("warning message")
