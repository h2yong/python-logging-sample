import asyncio
import logging
import os
import socket
from pathlib import Path
from typing import Any

import pytest
import shortuuid
import structlog

from app import structlog_utils
from sample.flask_with_structlog_sample import http_app


@pytest.mark.meta(notes="基础用法")
def test_structlog_base() -> None:
    logger = structlog.get_logger()
    """
    Structlog 支持以下日志级别：
    DEBUG: 调试信息。
    INFO: 正常事件。
    WARNING: 潜在问题。
    ERROR: 错误事件。
    CRITICAL: 严重问题。
    """
    logger.debug("调试信息")
    logger.info("正常事件")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重问题")


@pytest.mark.meta(notes="调试日志")
def test_structlog_dev_console() -> None:
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer()  # 用于调试，可打印彩色日志
        ]
    )
    logger = structlog.get_logger()
    logger.info("自定义日志格式")


@pytest.mark.meta(notes="JSON格式日志")
def test_structlog_json_renderer() -> None:
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),  # 方便集成到ELK
        ]
    )
    logger = structlog.get_logger()
    logger.info("JSON 格式日志")


def set_process_id(_: Any, __: Any, event_dict: dict[Any, Any]) -> dict[Any, Any]:
    event_dict["process_id"] = os.getpid()
    return event_dict


@pytest.mark.meta(notes="自定义event_dict字段")
def test_set_process_id() -> None:
    structlog.configure(
        processors=[
            set_process_id,
            structlog.processors.JSONRenderer()
        ],
    )
    logger = structlog.get_logger()
    logger.info("Create processors to modify events at runtime.")


@pytest.mark.meta(notes="异步日志记录")
async def log_async() -> None:
    logger = structlog.get_logger()
    await logger.awarning("异步日志记录")


asyncio.run(log_async())


def risky_div(x: float, y: float) -> float:
    return x / y


@pytest.mark.meta(notes="捕获异常信息")
def test_print_exception() -> None:
    logger = structlog.get_logger()
    try:
        risky_div(1, 0)
    except Exception as e:
        logger.error("处理过程中发生错误", exc_info=True)


@pytest.mark.meta(notes="bind上下文信息，上下文信息需要每次使用此logger_bind。")
def test_bind() -> None:
    logger = structlog.get_logger()
    logger_bind = logger.bind(user="alice", ip=socket.gethostbyname(socket.gethostname()))
    logger_bind.info("用户登录")


@pytest.mark.meta(notes="简易写文件")
def test_write_logger_factory() -> None:
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(ensure_ascii=False),
        ],
        logger_factory=structlog.WriteLoggerFactory(file=Path("app").with_suffix(".log").open("wt")),
    )

    logger = structlog.get_logger()
    logger.info("info message")
    logger.error("error message")


@pytest.mark.meta(notes="配置日志过滤")
def test_make_filtering_bound_logger() -> None:
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING))
    logger = structlog.get_logger()
    logger.info("这条消息不会显示")
    logger.warning("警告信息")


@pytest.mark.meta(notes="绑定上下文")
class ContextvarsSample:
    def __init__(self) -> None:
        self.logger = structlog_utils.get_logger(name=__name__)

    def a(self) -> None:
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(user="alice",
                                               ip=socket.gethostbyname(socket.gethostname()),
                                               request_id=shortuuid.uuid())
        self.logger.info("this is a function")

    def b(self) -> None:
        self.logger.info("this is b function")


def test_contextvars() -> None:
    ctx = ContextvarsSample()
    ctx.a()
    ctx.a()


# https://www.structlog.org/en/stable/frameworks.html#flask
@pytest.mark.meta(notes="在flask启动时绑定上下文")
def test_request_id() -> None:
    test_client = http_app.test_client()
    res = test_client.post(
        "/api/v1/test",
        json={"request_id": shortuuid.uuid()},
        headers={"Content-Type": "application/json"},
    )
    assert res.status_code == 200
