import json
import os
import sys

from typing import Any

import loguru._handler

from loguru import logger
from loguru._recattrs import RecordException


def _serialize_record(text: str, record: dict[Any, Any]) -> Any:
    """Loguru serialize 减少字段.

    :param text: loguru text
    :param record: loguru record
    :return: json序列化日志
    """
    exception: RecordException = record["exception"]
    if exception is not None:
        exception = RecordException(
            type=None if exception.type is None else exception.type.__name__,
            value=exception.value,
            traceback=bool(exception.traceback),
        )

    serializable = {
        "text": text,
        "record": {
            "extra": record["extra"],
            "time": record["time"],
            "exception": exception,
        },
    }
    return json.dumps(serializable, default=str, ensure_ascii=False) + "\n"


def get_logger(level: Any = "INFO",
               env_name: str = "ENV",
               dev_env_default_name: str = "development") -> Any:
    """获取logger.

    :param level: 程序处理的日志消息的最低级别, 值可以为"INFO"或者"logging.INFO"
    :param env_name: 开发或生产环境的环境变量key
    :param dev_env_default_name: 开发环境默认的环境变量值
    :return: logger
    """
    loguru._handler.Handler._serialize_record = staticmethod(_serialize_record)
    env: str = os.getenv(env_name, dev_env_default_name)
    if env != dev_env_default_name:
        logger.add(sys.stderr, serialize=True, enqueue=True, level=level)  # 非开发环境使用json格式，异步输出
    return logger.opt(lazy=True)
