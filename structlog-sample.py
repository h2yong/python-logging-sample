import asyncio
import logging
import os
import socket
from pathlib import Path

import structlog

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

# 自定义日志格式
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer()  # 可选，用于调试
    ]
)
logger.info("自定义日志格式")

# JSON格式日志
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)
logger.info("JSON 格式日志")


def set_process_id(_, __, event_dict):
    event_dict["process_id"] = os.getpid()
    return event_dict


structlog.configure(
    processors=[
        set_process_id,
        structlog.processors.JSONRenderer()
    ],
)
logger.info("Create processors to modify events at runtime.")


# 异步日志记录
async def log_async():
    await logger.awarning("异步日志记录")


asyncio.run(log_async())


def risky_div(x, y):
    return x / y


try:
    # 可能会抛出异常的代码
    risky_div(1, 0)
except Exception as e:
    logger.error("处理过程中发生错误", exc_info=True)

logger.info("hello, %s!", "world", key="value!", more_than_strings=[1, 2, 3])

# 额外的上下文信息
logger = logger.bind(user="alice", ip=socket.gethostbyname(socket.gethostname()))
logger.info("用户登录")

# 写文件
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.WriteLoggerFactory(file=Path("app").with_suffix(".log").open("wt")),
)

logger = structlog.get_logger()
logger.info("Info message")
logger.error("Error message")

# 配置日志过滤
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING))
logger.info("这条消息不会显示")
logger.warning("警告信息")
