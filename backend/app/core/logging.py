#!/usr/bin/env python3
"""
统一日志配置模块
提供项目统一的日志格式和配置
"""

import sys
import os
from pathlib import Path
from loguru import logger
from app.core.config import settings


def setup_logging():
    """
    设置项目统一的日志配置
    包含详细的模块名、文件名、行号等信息
    """
    # 移除默认的日志处理器
    logger.remove()
    
    # 确保日志目录存在
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 详细的日志格式，包含模块名、文件名、行号等信息
    detailed_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # 控制台输出 - 彩色格式
    logger.add(
        sys.stdout,
        format=detailed_format,
        level=settings.LOG_LEVEL,
        colorize=True,
        backtrace=True,
        diagnose=True,
        enqueue=True  # 多线程安全
    )
    
    # 文件输出 - 纯文本格式
    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    )
    
    # 应用主日志
    logger.add(
        "logs/app.log",
        rotation="1 day",
        retention="30 days",
        format=file_format,
        level=settings.LOG_LEVEL,
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    # 错误日志单独记录
    logger.add(
        "logs/error.log",
        rotation="1 day", 
        retention="30 days",
        format=file_format,
        level="ERROR",
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    # 调试日志（仅在DEBUG模式下）
    if settings.DEBUG:
        logger.add(
            "logs/debug.log",
            rotation="1 day",
            retention="7 days",
            format=file_format,
            level="DEBUG",
            encoding="utf-8",
            backtrace=True,
            diagnose=True,
            enqueue=True
        )
    
    # 性能日志（用于记录慢查询、API响应时间等）
    logger.add(
        "logs/performance.log",
        rotation="1 day",
        retention="7 days", 
        format=file_format,
        level="INFO",
        encoding="utf-8",
        filter=lambda record: "PERF" in record["extra"],
        enqueue=True
    )
    
    logger.info("日志系统初始化完成")


def get_logger(name: str = None):
    """
    获取带有模块名称的logger实例
    
    Args:
        name: 模块名称，如果不提供则自动获取调用者的模块名
        
    Returns:
        logger实例
    """
    if name is None:
        # 自动获取调用者的模块名
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'unknown')
    
    return logger.bind(module=name)


def log_performance(operation: str, duration: float, **kwargs):
    """
    记录性能日志
    
    Args:
        operation: 操作名称
        duration: 耗时（秒）
        **kwargs: 其他参数
    """
    logger.bind(PERF=True).info(
        f"PERFORMANCE | {operation} | Duration: {duration:.3f}s | {kwargs}"
    )


def log_api_request(method: str, path: str, status_code: int, duration: float, **kwargs):
    """
    记录API请求日志
    
    Args:
        method: HTTP方法
        path: 请求路径
        status_code: 状态码
        duration: 耗时（秒）
        **kwargs: 其他参数
    """
    level = "ERROR" if status_code >= 400 else "INFO"
    logger.log(
        level,
        f"API | {method} {path} | {status_code} | {duration:.3f}s | {kwargs}"
    )


def log_database_query(query: str, duration: float, **kwargs):
    """
    记录数据库查询日志
    
    Args:
        query: SQL查询语句
        duration: 耗时（秒）
        **kwargs: 其他参数
    """
    # 截断过长的查询语句
    short_query = query[:100] + "..." if len(query) > 100 else query
    
    if duration > 1.0:  # 慢查询
        logger.warning(f"SLOW_QUERY | {short_query} | Duration: {duration:.3f}s | {kwargs}")
    else:
        logger.debug(f"DB_QUERY | {short_query} | Duration: {duration:.3f}s | {kwargs}")
