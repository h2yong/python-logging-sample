import socket

import pytest
import shortuuid

from loguru import logger


@pytest.mark.meta(notes="基础用法")
def test_loguru_base() -> None:
    """Demonstrates the supported log levels in Structlog.

    Structlog 支持以下日志级别:
    DEBUG: 调试信息.
    INFO: 正常事件.
    WARNING: 潜在问题.
    ERROR: 错误事件.
    CRITICAL: 严重问题.
    """
    logger.debug("调试信息")
    logger.info("正常事件")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重问题")


@logger.catch
def risky_div(x: float, y: float) -> float:
    """Divide x by y and return the result.

    Parameters
    ----------
    x : float
        Numerator.
    y : float
        Denominator.

    Returns
    -------
    float
        The result of x divided by y.

    Raises
    ------
    ZeroDivisionError
        If y is zero.

    """
    return x / y


@pytest.mark.meta(notes="捕获异常")
def test_print_exception() -> None:
    """Test that risky_div logs and catches exceptions as expected."""
    risky_div(1, 0)


@pytest.mark.meta(notes="bind上下文信息, 上下文信息需要每次使用此logger_bind")
def test_bind() -> None:
    """Test binding context information to the logger and logging a user login event."""
    logger_bind = logger.bind(user="alice", ip=socket.gethostbyname(socket.gethostname()))
    logger_bind.info("用户登录")


@pytest.mark.meta(notes="延迟日志")
def test_lazy() -> None:
    """Test lazy evaluation of log messages using logger.opt(lazy=True)."""
    logger.opt(lazy=True).info("结果: {res}", res=lambda: sum(range(10**7)))


def a() -> None:
    """Configure logger with a unique request_id and log a message."""
    logger.configure(extra={"request_id": shortuuid.uuid()})
    logger.info("a message")


def b() -> None:
    """Log a message indicating function b was called."""
    logger.info("b message")


@pytest.mark.meta(notes="绑定上下文")
def test_extra() -> None:
    """Test logging with extra context by calling functions a and b."""
    a()
    b()


@pytest.mark.meta(notes="程序处理的日志消息的最低级别")
def test_filter() -> None:
    """Test setting the minimum log level for processed log messages and writing logs to a file."""
    # 终端显示不受该段代码设置
    # 添加一个日志处理器, 输出到文件
    # 设置日志最低显示级别为INFO, format将设置sink中的内容
    # sink链接的本地文件, 如不存在则新建。如果存在则追写
    logger.add(sink="app_{time:YYYY-MM-DD}.log", level="INFO", format="{time:HH:mm:ss}  | {message}| {level}")

    # debug结果不被显示到本地文件
    logger.debug("这是一条调试信息")
    logger.info("这是一条普通信息")


@pytest.mark.meta(notes="文件日志(每天滚动, 保留 3 天, 压缩为 zip)")
def test_write_file() -> None:
    """Test writing logs to a file with daily rotation, 3-day retention, zip compression, and JSON serialization."""
    logger.add(
        "app_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="3 days",
        compression="zip",
        format="{time:HH:mm:ss} | {level} | {message}",
        serialize=True,  # json格式日志
        enqueue=True,  # 异步日志
    )

    logger.info(f"{shortuuid.uuid()} message")
