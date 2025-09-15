# python logging 包 sample

此项目为 python 第三方 logging 包 sample。

## [loguru](https://github.com/Delgan/loguru) 核心功能一览

| 功能               | 描述                                                          |
| ------------------ | ------------------------------------------------------------- |
| 开箱即用           | 直接输出到 stderr，无需 boilerplate                           |
| 轮转 & 保留 & 压缩 | `rotation="500 MB",retention="7 days",compression="zip"`      |
| 彩色 & 美化        | 支持 <green>...</green> 标记，终端自动渲染                    |
| 完整异常捕获       | `@logger.catch`装饰器 + `backtrace=True`，堆栈变量全展示      |
| 结构化 & JSON      | `serialize=True`，输出 JSON，方便 ELK / Splunk                |
| 延迟执行           | opt(lazy=True)，昂贵操作仅在需要时才评估                      |
| 额外的上下文信息   | `logger.bind`, 使用 bind 方法向日志记录器添加额外的上下文信息 |

**参考文档:**
* [Python日志记录库loguru使用指北](https://www.cnblogs.com/luohenyueji/p/18276299)
* [loguru serialize 减少字段](https://segmentfault.com/a/1190000042389458)

## [structlog](https://github.com/hynek/structlog/)

**参考文档：**
* [structlog documentation](https://www.structlog.org/en/stable/index.html)
* [A Comprehensive Guide to Python Logging with Structlog](https://betterstack.com/community/guides/logging/structlog/)
* [使用structlog实现多格式日志输出：控制台与文件分离](https://blog.gitcode.com/ea3779cf0bac55d770e255d5e0fb2893.html)