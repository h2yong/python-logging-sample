import logging

import pytest

from app import logging_utils


@pytest.mark.meta(notes="基础功能")
def test_logging_utils()-> None:
    logger = logging_utils.get_logger(channel="test")
    logger.info("this is info.")


@pytest.mark.meta(notes="重置logger.handlers")
def test_logging_utils_with_handlers() -> None:
    log = logging.getLogger("app")
    stream_handler = logging.StreamHandler()
    log.addHandler(stream_handler)
    log.setLevel("info".upper())
    logger = logging_utils.get_logger(logger=log, channel="test")
    logger.warning("this is warning.")
