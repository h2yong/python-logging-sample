import os

import pytest

from app import loguru_utils
from sample.test_loguru_sample import risky_div


@pytest.mark.meta(notes="基础功能")
def test_structlog_utils() -> None:
    os.environ["ENV"] = "development"
    logger = loguru_utils.get_logger()
    logger.info("info message")

    os.environ["ENV"] = "production"
    log = loguru_utils.get_logger()
    log.warning("warning message")


@pytest.mark.meta(notes="捕获异常")
def test_print_exception() -> None:
    risky_div(1, 0)
