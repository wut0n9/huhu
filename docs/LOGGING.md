# 日志系统使用指南

## 概述

项目使用 `loguru` 作为日志库，提供了统一的日志格式和配置，包含详细的模块名称、文件名称、行号等信息。

## 日志格式

### 控制台输出格式（彩色）
```
2025-08-01 11:39:00.034 | INFO     | app.core.database:init_db:21 | 数据库初始化完成
```

### 文件输出格式（纯文本）
```
2025-08-01 11:39:00.034 | INFO     | app.core.database:init_db:21 | 数据库初始化完成
```

格式说明：
- `时间戳`：精确到毫秒
- `日志级别`：DEBUG、INFO、WARNING、ERROR
- `模块名:函数名:行号`：精确定位日志来源
- `消息内容`：实际的日志信息

## 日志文件

项目会自动创建以下日志文件：

### 1. 应用主日志 (`logs/app.log`)
- 记录所有级别的日志
- 按天轮转，保留30天
- 包含所有应用活动

### 2. 错误日志 (`logs/error.log`)
- 仅记录ERROR级别的日志
- 按天轮转，保留30天
- 便于快速定位错误

### 3. 性能日志 (`logs/performance.log`)
- 记录性能相关的日志
- 包含API响应时间、数据库查询时间等
- 用于性能监控和优化

### 4. 调试日志 (`logs/debug.log`)
- 仅在DEBUG模式下生成
- 记录详细的调试信息
- 保留7天

## 使用方法

### 1. 基本使用

```python
from app.core.logging import get_logger

# 获取当前模块的logger
logger = get_logger(__name__)

# 记录不同级别的日志
logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")

# 记录异常（包含完整堆栈跟踪）
try:
    # 一些可能出错的代码
    pass
except Exception as e:
    logger.exception("操作失败")
```

### 2. 性能日志

```python
from app.core.logging import log_performance
import time

start_time = time.time()
# 执行一些操作
duration = time.time() - start_time

log_performance(
    "数据库查询",
    duration,
    table="users",
    rows=100
)
```

### 3. API请求日志

```python
from app.core.logging import log_api_request

log_api_request(
    method="POST",
    path="/api/v1/auth/login",
    status_code=200,
    duration=0.456,
    client_ip="192.168.1.100"
)
```

### 4. 数据库查询日志

```python
from app.core.logging import log_database_query

log_database_query(
    "SELECT * FROM users WHERE active = 1",
    0.123,
    table="users",
    rows_affected=150
)
```

## 日志中间件

项目包含了自动记录API请求的中间件：

### 功能特性
- 自动记录所有HTTP请求
- 包含请求方法、路径、状态码、响应时间
- 记录客户端IP地址
- 自动隐藏敏感信息（密码、token等）
- 可配置跳过某些路径（如健康检查）

### 配置
```python
# 在main.py中已自动配置
app.add_middleware(LoggingMiddleware)
```

## 配置选项

### 环境变量
- `LOG_LEVEL`：日志级别（DEBUG、INFO、WARNING、ERROR）
- `DEBUG`：是否启用调试模式

### 自定义配置
可以在 `app/core/logging.py` 中修改：
- 日志格式
- 文件轮转策略
- 保留天数
- 输出目标

## 最佳实践

### 1. 日志级别使用
- `DEBUG`：详细的调试信息，仅在开发时使用
- `INFO`：一般信息，记录正常的业务流程
- `WARNING`：警告信息，可能的问题但不影响运行
- `ERROR`：错误信息，需要关注和处理的问题

### 2. 日志内容
- 使用有意义的消息
- 包含必要的上下文信息
- 避免记录敏感信息
- 使用结构化的日志格式

### 3. 性能考虑
- 避免在循环中记录大量日志
- 使用适当的日志级别
- 考虑异步日志记录（已启用）

## 监控和告警

### 日志监控
- 可以使用ELK Stack、Grafana等工具监控日志
- 设置错误日志告警
- 监控性能日志中的慢查询

### 日志分析
- 使用grep、awk等工具分析日志文件
- 定期清理过期日志文件
- 监控日志文件大小

## 示例代码

参考 `app/core/logging_example.py` 文件查看完整的使用示例。
