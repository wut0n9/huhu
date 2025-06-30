# MCP Client服务 - SSE连接版本
# 参考：https://modelcontextprotocol.io/quickstart/client
# 依赖：pip install mcp

import asyncio
import json
from typing import Any, Dict, List, Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, types
from mcp.client.sse import sse_client
from app.core.config import settings
from loguru import logger

class MCPClientService:
    def __init__(self):
        """初始化MCP客户端服务"""
        self.service_sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()
        self.running = True
        self._tools_cache: Dict[str, List[Dict]] = {}

    async def add_service_session(self, server_name: str, server_url: str):
        """
        添加新的服务会话
        
        Args:
            server_name: 服务名称
            server_url: MCP服务器URL
        """
        try:
            logger.info(f"开始连接到服务 {server_name}，URL: {server_url}")
            
            # 创建SSE连接并管理其生命周期
            logger.info("正在建立SSE连接...")
            stdio_transport = await self.exit_stack.enter_async_context(sse_client(server_url))
            
            logger.info("SSE连接已建立，正在创建会话...")
            session = await self.exit_stack.enter_async_context(
                ClientSession(*stdio_transport, sampling_callback=self._handle_sampling_message)
            )
            
            logger.info("正在初始化会话...")
            await session.initialize()
            logger.info("会话初始化成功")
            
            self.service_sessions[server_name] = session
            logger.info(f"成功连接到服务: {server_name}")
            
        except Exception as e:
            logger.error(f"连接服务 {server_name} 失败: {str(e)}")
            raise

    async def remove_service_session(self, server_name: str):
        """
        移除服务会话
        
        Args:
            server_name: 要移除的服务名称
        """
        if server_name in self.service_sessions:
            del self.service_sessions[server_name]
            # 不需要手动关闭连接，AsyncExitStack会处理

    async def update_service_session(self, server_name: str, server_url: str):
        """
        更新服务会话
        
        Args:
            server_name: 服务名称
            server_url: 新的MCP服务器URL
        """
        # 如果服务已存在，先移除
        if server_name in self.service_sessions:
            await self.remove_service_session(server_name)
        # 添加新的服务会话
        await self.add_service_session(server_name, server_url)

    async def get_service_session(self, server_name: str) -> Optional[ClientSession]:
        """
        获取服务会话
        
        Args:
            server_name: 服务名称
            
        Returns:
            ClientSession: 服务会话实例
        """
        return self.service_sessions.get(server_name)

    async def list_available_services(self) -> List[str]:
        """
        列出所有可用的服务名称
        
        Returns:
            list: 服务名称列表
        """
        return list(self.service_sessions.keys())

    async def list_tools(self, server_name: Optional[str] = None) -> List[Dict]:
        """
        获取工具列表
        
        Args:
            server_name: 指定服务器名称，如果为None则获取所有服务器的工具
            
        Returns:
            List[Dict]: 工具列表
        """
        if server_name:
            if server_name not in self.service_sessions:
                raise ValueError(f"服务 {server_name} 不存在")
            
            if server_name not in self._tools_cache:
                session = self.service_sessions[server_name]
                response = await session.list_tools()
                self._tools_cache[server_name] = [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    } for tool in response.tools
                ]
            return self._tools_cache[server_name]
        else:
            # 获取所有服务器的工具
            all_tools = []
            for name in self.service_sessions.keys():
                tools = await self.list_tools(name)
                for tool in tools:
                    tool["server_name"] = name
                all_tools.extend(tools)
            return all_tools

    async def call_tool(self, server_name: str, tool_name: str, tool_args: Dict) -> Any:
        """
        调用指定工具
        
        Args:
            server_name: 服务器名称
            tool_name: 工具名称
            tool_args: 工具参数
            
        Returns:
            Any: 工具调用结果
        """
        if server_name not in self.service_sessions:
            raise ValueError(f"服务 {server_name} 不存在")
        
        session = self.service_sessions[server_name]
        result = await session.call_tool(tool_name, tool_args)
        return result

    async def cleanup(self):
        """清理所有资源"""
        self.running = False
        await self.exit_stack.aclose()
        self.service_sessions.clear()
        self._tools_cache.clear()

    async def _handle_sampling_message(self, message: types.CreateMessageRequestParams) -> Optional[types.CreateMessageResult]:
        """
        处理MCP服务器的采样消息
        
        Args:
            message: 包含服务器发送的采样消息参数
            
        Returns:
            CreateMessageResult: 标准化的响应格式
        """
        try:
            logger.debug(f"收到采样消息: {message}")
            # 处理中间生成结果
            if message.content and message.content.text:
                # 可以在这里添加自定义处理逻辑
                processed_text = message.content.text
                logger.debug(f"收到采样消息: {processed_text}")
                
                # 根据消息状态决定是否继续
                stop_reason = "endTurn" if message.is_final else "continue"
                logger.debug(f"消息状态: {stop_reason}")
                
                return types.CreateMessageResult(
                    role="assistant",
                    content=types.TextContent(
                        type="text",
                        text=processed_text,
                    ),
                    model=settings.LLM_MODEL,
                    stopReason=stop_reason,
                )
            return None
        except Exception as e:
            logger.error(f"处理采样消息时出错: {str(e)}")
            return None

# 全局MCP Client实例管理
_mcp_client: Optional[MCPClientService] = None

async def get_mcp_client() -> MCPClientService:
    """获取全局MCP Client实例"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClientService()
    return _mcp_client

async def close_mcp_client():
    """关闭全局MCP Client连接"""
    global _mcp_client
    if _mcp_client:
        await _mcp_client.cleanup()
        _mcp_client = None 