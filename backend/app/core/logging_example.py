#!/usr/bin/env python3
"""
日志使用示例
演示如何在项目中使用新的日志系统
"""

from app.core.logging import get_logger, log_performance, log_api_request, log_database_query
import time

# 获取当前模块的logger
logger = get_logger(__name__)

def example_service_function():
    """示例服务函数"""
    logger.info("开始执行服务函数")
    
    try:
        # 模拟一些业务逻辑
        logger.debug("正在处理业务逻辑...")
        
        # 模拟数据库查询
        start_time = time.time()
        # ... 数据库操作 ...
        query_time = time.time() - start_time
        
        # 记录数据库查询日志
        log_database_query(
            "SELECT * FROM users WHERE active = 1",
            query_time,
            table="users",
            rows_affected=150
        )
        
        # 模拟性能监控
        operation_time = time.time() - start_time
        log_performance(
            "用户数据处理",
            operation_time,
            users_count=150,
            cache_hit=True
        )
        
        logger.info("服务函数执行成功")
        return {"status": "success", "count": 150}
        
    except Exception as e:
        logger.exception("服务函数执行失败")
        raise

def example_api_endpoint():
    """示例API端点"""
    start_time = time.time()
    
    try:
        # 模拟API处理逻辑
        result = example_service_function()
        
        # 记录API请求日志
        duration = time.time() - start_time
        log_api_request(
            "GET",
            "/api/v1/users",
            200,
            duration,
            client_ip="192.168.1.100",
            user_id=123
        )
        
        return result
        
    except Exception as e:
        # 记录错误的API请求
        duration = time.time() - start_time
        log_api_request(
            "GET",
            "/api/v1/users",
            500,
            duration,
            client_ip="192.168.1.100",
            error=str(e)
        )
        raise

if __name__ == "__main__":
    # 示例用法
    from app.core.logging import setup_logging
    
    # 初始化日志系统
    setup_logging()
    
    print("=== 日志使用示例 ===")
    
    # 基本日志记录
    logger.debug("这是调试信息")
    logger.info("这是普通信息")
    logger.warning("这是警告信息")
    logger.error("这是错误信息")
    
    # 业务逻辑日志
    try:
        result = example_api_endpoint()
        logger.info(f"API调用成功: {result}")
    except Exception as e:
        logger.error(f"API调用失败: {e}")
    
    print("=== 示例完成 ===")
    print("请查看logs目录下的日志文件：")
