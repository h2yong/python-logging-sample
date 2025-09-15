import inspect
import socket

import allure
import shortuuid
from loguru import logger


@allure.story("基础用法")
def test_loguru_base():
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


@logger.catch
def risky_div(x, y):
    return x / y


@allure.story("捕获异常")
def test_print_exception():
    risky_div(1, 0)


@allure.story("bind上下文信息，上下文信息需要每次使用此logger_bind")
def test_bind():
    logger_bind = logger.bind(user="alice", ip=socket.gethostbyname(socket.gethostname()))
    logger_bind.info("用户登录")


@allure.story("延迟日志")
def test_lazy():
    logger.opt(lazy=True).info("结果：{res}", res=lambda: sum(range(10 ** 7)))


def a():
    logger.configure(extra={"request_id": shortuuid.uuid()})
    logger.info("a message")


def b():
    logger.info("b message")


@allure.story("绑定上下文")
def test_extra():
    a()
    b()


@allure.story("程序处理的日志消息的最低级别")
def test_filter():
    # 终端显示不受该段代码设置
    # 添加一个日志处理器，输出到文件
    # 设置日志最低显示级别为INFO，format将设置sink中的内容
    # sink链接的本地文件，如不存在则新建。如果存在则追写
    logger.add(sink="app_{time:YYYY-MM-DD}.log", level="INFO", format="{time:HH:mm:ss}  | {message}| {level}")

    # debug结果不被显示到本地文件
    logger.debug("这是一条调试信息")
    logger.info("这是一条普通信息")


@allure.story("文件日志（每天滚动，保留 3 天，压缩为 zip）")
def test_write_file():
    logger.add(
        "app_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="3 days",
        compression="zip",
        format="{time:HH:mm:ss} | {level} | {message}",
        serialize=True,  # json格式日志
        enqueue=True # 异步日志
    )

    logger.info(f"{inspect.currentframe().f_code.co_name} message")
