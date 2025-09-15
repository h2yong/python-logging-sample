import asyncio
import logging
import os
import socket
from pathlib import Path

import allure
import shortuuid
import structlog

from app import structlog_utils


@allure.story("基础用法")
def test_structlog_base():
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


@allure.story("调试日志")
def test_structlog_dev_console():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer()  # 用于调试，可打印彩色日志
        ]
    )
    logger = structlog.get_logger()
    logger.info("自定义日志格式")


@allure.story("JSON格式日志")
def test_structlog_json_renderer():
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),  # 方便集成到ELK
        ]
    )
    logger = structlog.get_logger()
    logger.info("JSON 格式日志")


def set_process_id(_, __, event_dict):
    event_dict["process_id"] = os.getpid()
    return event_dict


@allure.story("自定义event_dict字段")
def test_set_process_id():
    structlog.configure(
        processors=[
            set_process_id,
            structlog.processors.JSONRenderer()
        ],
    )
    logger = structlog.get_logger()
    logger.info("Create processors to modify events at runtime.")


@allure.story("异步日志记录")
async def log_async():
    logger = structlog.get_logger()
    await logger.awarning("异步日志记录")


asyncio.run(log_async())


def risky_div(x, y):
    return x / y


@allure.story("捕获异常信息")
def test_print_exception():
    logger = structlog.get_logger()
    try:
        risky_div(1, 0)
    except Exception as e:
        logger.error("处理过程中发生错误", exc_info=True)


@allure.story("bind上下文信息，上下文信息需要每次使用此logger_bind。")
def test_bind():
    logger = structlog.get_logger()
    logger_bind = logger.bind(user="alice", ip=socket.gethostbyname(socket.gethostname()))
    logger_bind.info("用户登录")


@allure.story("简易写文件")
def test_write_logger_factory():
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


@allure.story("配置日志过滤")
def test_make_filtering_bound_logger():
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING))
    logger = structlog.get_logger()
    logger.info("这条消息不会显示")
    logger.warning("警告信息")


@allure.story("绑定上下文")
class ContextvarsSample:
    def __init__(self):
        self.logger = structlog_utils.get_logger(name=__name__)

    def a(self):
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(user="alice",
                                               ip=socket.gethostbyname(socket.gethostname()),
                                               request_id=shortuuid.uuid())
        self.logger.info("this is a function")

    def b(self):
        self.logger.info("this is b function")


def test_contextvars():
    ctx = ContextvarsSample()
    ctx.a()
    ctx.a()
