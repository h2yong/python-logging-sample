import socket

from loguru import logger

# 1. 控制台输出
logger.debug("调试信息：x = {x}", x=42)

# 2. 文件日志（每天滚动，保留 3 天，压缩为 zip）
logger.add(
    "app_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="3 days",
    compression="zip",
    format="{time:HH:mm:ss} | {level} | {message}",
    serialize=True,  # 结构化日志
    enqueue=True
)


# 3. 捕获异常
@logger.catch
def risky_div(x, y):
    return x / y


risky_div(1, 0)

# 4. bind上下文信息
logger_bind = logger.bind(user="alice", ip=socket.gethostbyname(socket.gethostname()))
logger_bind.info("用户登录")

# 5. 延迟日志
logger.opt(lazy=True).info("结果：{res}", res=lambda: sum(range(10 ** 7)))


# 6. 绑定上下文，如请求request_id，不需要调用bind logger
def a():
    import shortuuid
    logger.configure(extra={"request_id": shortuuid.uuid()})
    logger.info("a message")


def b():
    logger.info("b message")


if __name__ == "__main__":
    a()
    b()
