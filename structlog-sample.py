import asyncio
import logging
import os
import socket
from pathlib import Path

import shortuuid
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

# 1. 自定义日志格式
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer()  # 用于调试，可打印彩色日志
    ]
)
logger.info("自定义日志格式")

# 2. JSON格式日志
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),  # 方便集成到ELK
    ]
)
logger.info("JSON 格式日志")


# 3. 举例说明自定义字段
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


# 4. 异步日志记录
async def log_async():
    await logger.awarning("异步日志记录")


asyncio.run(log_async())


# 6. 捕获异常信息
def risky_div(x, y):
    return x / y


try:
    # 可能会抛出异常的代码
    risky_div(1, 0)
except Exception as e:
    logger.error("处理过程中发生错误", exc_info=True)

logger.info("hello, %s!", "world", key="value!", more_than_strings=[1, 2, 3])

# 6. bind上下文信息，上下文信息需要每次使用此logger_bind。
logger_bind = logger.bind(user="alice", ip=socket.gethostbyname(socket.gethostname()))
logger_bind.info("用户登录")

# 7. 简易写文件
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

# 8. 配置日志过滤
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING))
logger.info("这条消息不会显示")
logger.warning("警告信息")

# 9. 绑定上下文，如请求request_id，不需要调用bind logger
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.THREAD_NAME
            }
        ),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(),
    context_class=dict,
    cache_logger_on_first_use=False,
)


def a():
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(user="alice",
                                           ip=socket.gethostbyname(socket.gethostname()),
                                           request_id=shortuuid.uuid())
    logger.info("this is a function")


def b():
    logger.info("this is b function")


if __name__ == "__main__":
    a()
    b()
