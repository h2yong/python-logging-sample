import logging
import os
import sys

from typing import Any

import structlog


def get_logger(name: str = "base",
               level: Any = logging.INFO,
               env_name: str = "ENV",
               dev_env_default_name: str = "development") -> Any:
    """获取logger.

    :param name: 日志名称
    :param level: 程序处理的日志消息的最低级别, 值可以为"INFO"或者"logging.INFO"
    :param env_name: 开发或生产环境的环境变量key
    :param dev_env_default_name: 开发环境默认的环境变量值
    :return: logger
    """
    env: str = os.getenv(env_name, dev_env_default_name)
    if env == dev_env_default_name:
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
                        structlog.processors.CallsiteParameter.THREAD_NAME,
                    }
                ),
                structlog.dev.ConsoleRenderer(),  # 开发环境使用带颜色console
            ],
            logger_factory=structlog.PrintLoggerFactory(),
            context_class=dict,
            cache_logger_on_first_use=False,
        )
    else:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.processors.CallsiteParameterAdder(
                    {
                        structlog.processors.CallsiteParameter.FILENAME,
                        structlog.processors.CallsiteParameter.FUNC_NAME,
                        structlog.processors.CallsiteParameter.LINENO,
                        structlog.processors.CallsiteParameter.THREAD_NAME,
                    }
                ),
                structlog.processors.JSONRenderer(ensure_ascii=False),  # 非开发环境使用json格式日志
            ],
            wrapper_class=structlog.make_filtering_bound_logger(level),
            logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
            context_class=dict,
            cache_logger_on_first_use=False,
        )

    return structlog.get_logger(name)
