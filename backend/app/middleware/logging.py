#!/usr/bin/env python3
"""
日志中间件
记录API请求和响应信息
"""

import time
import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import get_logger, log_api_request

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    API请求日志中间件
    记录所有HTTP请求的详细信息
    """
    
    def __init__(self, app, skip_paths: list = None, streaming_paths: list = None, enabled: bool = True):
        """
        初始化日志中间件

        Args:
            app: FastAPI应用实例
            skip_paths: 跳过记录的路径列表
            streaming_paths: 流式响应路径列表，这些路径不会读取request body
            enabled: 是否启用中间件（可用于开发环境禁用）
        """
        super().__init__(app)
        self.enabled = enabled
        self.skip_paths = skip_paths or ["/ping", "/health", "/metrics"]
        self.streaming_paths = streaming_paths or ["/api/v1/agent/chat"]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        处理HTTP请求并记录日志

        Args:
            request: HTTP请求对象
            call_next: 下一个中间件或路由处理器

        Returns:
            HTTP响应对象
        """
        # 如果中间件被禁用，直接传递请求
        if not self.enabled:
            return await call_next(request)

        # 跳过某些路径的日志记录
        if request.url.path in self.skip_paths:
            return await call_next(request)
        
        # 记录请求开始时间
        start_time = time.time()
        
        # 获取请求信息
        method = request.method
        path = request.url.path
        query_params = str(request.query_params) if request.query_params else ""
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "")
        
        # 记录请求体（仅对POST/PUT/PATCH请求，且不是流式响应路径）
        request_body = None
        is_streaming_path = any(path in request.url.path for path in self.streaming_paths)

        if method in ["POST", "PUT", "PATCH"] and not is_streaming_path:
            try:
                body = await request.body()
                if body:
                    # 尝试解析JSON
                    try:
                        request_body = json.loads(body.decode())
                        # 隐藏敏感信息
                        request_body = self._mask_sensitive_data(request_body)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        request_body = f"<binary data: {len(body)} bytes>"

                # 安全地重新构造request，保持ASGI协议兼容性
                original_receive = request._receive
                body_sent = False

                async def safe_receive():
                    nonlocal body_sent
                    if not body_sent:
                        body_sent = True
                        return {"type": "http.request", "body": body}
                    else:
                        # 对于后续调用，使用原始的receive
                        return await original_receive()

                request._receive = safe_receive
            except Exception as e:
                logger.warning(f"读取请求体失败: {e}")
        elif is_streaming_path:
            logger.debug(f"跳过流式响应路径的请求体读取: {path}")
        
        # 记录请求开始
        logger.info(
            f"REQUEST_START | {method} {path} | IP: {client_ip} | "
            f"Query: {query_params} | UA: {user_agent[:50]}..."
        )
        
        if request_body:
            logger.debug(f"REQUEST_BODY | {method} {path} | {request_body}")
        
        # 处理请求
        try:
            response = await call_next(request)
            
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 记录响应信息
            status_code = response.status_code
            
            # 使用统一的API日志记录函数
            log_api_request(
                method=method,
                path=path,
                status_code=status_code,
                duration=process_time,
                client_ip=client_ip,
                query_params=query_params
            )
            
            # 添加响应头
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # 记录异常
            process_time = time.time() - start_time
            logger.error(
                f"REQUEST_ERROR | {method} {path} | Error: {str(e)} | "
                f"Duration: {process_time:.3f}s | IP: {client_ip}"
            )
            raise
    
    def _get_client_ip(self, request: Request) -> str:
        """
        获取客户端真实IP地址
        
        Args:
            request: HTTP请求对象
            
        Returns:
            客户端IP地址
        """
        # 检查代理头
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # 返回直接连接的IP
        return request.client.host if request.client else "unknown"
    
    def _mask_sensitive_data(self, data: dict) -> dict:
        """
        隐藏敏感数据
        
        Args:
            data: 原始数据字典
            
        Returns:
            隐藏敏感信息后的数据字典
        """
        if not isinstance(data, dict):
            return data
        
        sensitive_keys = {
            "password", "passwd", "pwd", "secret", "token", "key", 
            "api_key", "access_token", "refresh_token", "authorization"
        }
        
        masked_data = {}
        for key, value in data.items():
            if key.lower() in sensitive_keys:
                masked_data[key] = "***MASKED***"
            elif isinstance(value, dict):
                masked_data[key] = self._mask_sensitive_data(value)
            elif isinstance(value, list):
                masked_data[key] = [
                    self._mask_sensitive_data(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                masked_data[key] = value
        
        return masked_data
