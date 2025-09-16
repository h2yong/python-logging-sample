import os

import pytest

from app import structlog_utils


@pytest.mark.meta(notes="基础功能")
def test_structlog_utils() -> None:
    os.environ["ENV"] = "development"
    logger = structlog_utils.get_logger(name=__name__)
    logger.info("info message")

    os.environ["ENV"] = "production"
    log = structlog_utils.get_logger(name=__name__)
    log.warning("warning message")
