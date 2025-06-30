#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Agent服务类 - 支持MCP工具调用的智能对话代理
集成LLM大模型和MCP工具调用功能
"""

import json
import uuid
from typing import Dict, Any, List, Optional, AsyncGenerator
from openai import OpenAI
from app.core.config import settings
from app.services.mcp_client import get_mcp_client
from app.schemas.agent import Message, MessageRole, StreamChatResponse
from loguru import logger

class AgentService:
    def __init__(self):
        """
        初始化Agent服务
        
        Args:
            llm_client: LLM客户端实例
        """
        # 初始化LLM客户端
        self.llm_client = OpenAI(
            api_key=settings.LLM_API_KEY or settings.OPENAI_API_KEY,
            base_url=settings.LLM_BASE_URL or settings.OPENAI_BASE_URL
        )
        self.model = settings.LLM_MODEL or settings.OPENAI_MODEL
        
        # 对话历史管理
        self.conversations: Dict[str, List[Message]] = {}
        
        # MCP客户端
        self.mcp_client = None
        
    async def _get_mcp_client(self):
        """获取MCP客户端实例"""
        if self.mcp_client is None:
            self.mcp_client = await get_mcp_client()
        return self.mcp_client

    async def add_mcp_server(self, server_name: str, server_url: str):
        """
        添加MCP服务器
        
        Args:
            server_name: 服务器名称
            server_url: 服务器URL
        """
        mcp_client = await self._get_mcp_client()
        await mcp_client.add_service_session(server_name, server_url)
        logger.info(f"已添加MCP服务器: {server_name}")

    async def remove_mcp_server(self, server_name: str):
        """
        移除MCP服务器
        
        Args:
            server_name: 服务器名称
        """
        mcp_client = await self._get_mcp_client()
        await mcp_client.remove_service_session(server_name)
        logger.info(f"已移除MCP服务器: {server_name}")

    async def list_mcp_servers(self) -> List[str]:
        """
        列出所有MCP服务器
        
        Returns:
            List[str]: 服务器名称列表
        """
        mcp_client = await self._get_mcp_client()
        return await mcp_client.list_available_services()

    async def list_available_tools(self) -> List[Dict]:
        """
        列出所有可用工具
        
        Returns:
            List[Dict]: 工具列表
        """
        mcp_client = await self._get_mcp_client()
        return await mcp_client.list_tools()

    def _get_conversation_history(self, conversation_id: str) -> List[Message]:
        """
        获取对话历史
        
        Args:
            conversation_id: 对话ID
            
        Returns:
            List[Message]: 对话历史
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        return self.conversations[conversation_id]

    def _add_message_to_history(self, conversation_id: str, message: Message):
        """
        添加消息到对话历史
        
        Args:
            conversation_id: 对话ID
            message: 消息对象
        """
        history = self._get_conversation_history(conversation_id)
        history.append(message)
        
        # 限制历史长度
        if len(history) > settings.AGENT_MAX_HISTORY:
            history.pop(0)

    async def process_query(
        self, 
        query: str, 
        conversation_id: Optional[str] = None,
        stream: bool = False
    ) -> AsyncGenerator[StreamChatResponse, None]:
        """
        处理用户查询，支持多轮流式工具调用
        
        Args:
            query: 用户查询
            conversation_id: 对话ID
            stream: 是否使用流式响应
            
        Yields:
            StreamChatResponse: 流式响应
        """
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
        
        # 添加用户消息到历史
        user_message = Message(role=MessageRole.USER, content=query)
        self._add_message_to_history(conversation_id, user_message)
        
        # 获取对话历史
        messages = self._get_conversation_history(conversation_id)
        
        # 转换为LLM格式
        llm_messages = self._convert_messages_to_llm_format(messages)
        
        # 获取可用工具
        available_tools = await self._get_available_tools_for_llm()
        
        max_tool_rounds = settings.MCP_MAX_TOOL_ROUNDS
        final_answer = ""
        
        for round_idx in range(max_tool_rounds):
            logger.info(f"开始第 {round_idx + 1} 轮工具调用")
            
            # 调用LLM
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=llm_messages,
                tools=available_tools,
                tool_choice="auto",
                stream=stream,
                temperature=settings.MCP_TEMPERATURE
            )
            
            if stream:
                # 流式处理
                collected_messages = []
                tool_call_accumulators = {}
                tool_call_id = None
                
                for chunk in response:
                    delta = chunk.choices[0].delta
                    
                    # 收集普通内容
                    if hasattr(delta, "content") and delta.content:
                        collected_messages.append(delta.content)
                        yield StreamChatResponse(
                            conversation_id=conversation_id,
                            content=delta.content,
                            is_final=False
                        )
                    
                    # 收集工具调用
                    if hasattr(delta, "tool_calls") and delta.tool_calls:
                        for tool_call_delta in delta.tool_calls:
                            tool_call_id = tool_call_delta.id if tool_call_delta.id else tool_call_id
                            if tool_call_id not in tool_call_accumulators:
                                tool_call_accumulators[tool_call_id] = {
                                    "name": "",
                                    "arguments": ""
                                }
                            if hasattr(tool_call_delta.function, "name") and tool_call_delta.function.name:
                                tool_call_accumulators[tool_call_id]["name"] = tool_call_delta.function.name
                            if hasattr(tool_call_delta.function, "arguments") and tool_call_delta.function.arguments:
                                tool_call_accumulators[tool_call_id]["arguments"] += tool_call_delta.function.arguments
                
                # 执行工具调用
                if tool_call_accumulators:
                    tool_calls = []
                    for tool_call_id, tool_call in tool_call_accumulators.items():
                        function_name = tool_call["name"]
                        try:
                            tool_args = json.loads(tool_call["arguments"])
                        except Exception as e:
                            logger.error(f"解析工具参数失败: {tool_call['arguments']}, 错误: {e}")
                            continue
                        
                        # 执行工具调用
                        result = await self._execute_tool_call(function_name, tool_args)
                        
                        tool_calls.append({
                            "id": tool_call_id,
                            "name": function_name,
                            "arguments": tool_args,
                            "result": result
                        })
                    
                    # 更新对话历史
                    assistant_message = Message(
                        role=MessageRole.ASSISTANT,
                        content=None,
                        tool_calls=[{
                            "id": tool_call_id,
                            "type": "function",
                            "function": {
                                "name": tool_call["name"],
                                "arguments": json.dumps(tool_call["arguments"], ensure_ascii=False)
                            }
                        } for tool_call_id, tool_call in tool_call_accumulators.items()]
                    )
                    self._add_message_to_history(conversation_id, assistant_message)
                    
                    # 添加工具响应到历史
                    for tool_call in tool_calls:
                        tool_message = Message(
                            role=MessageRole.TOOL,
                            name=tool_call["name"],
                            tool_call_id=tool_call["id"],
                            content=str(tool_call["result"])
                        )
                        self._add_message_to_history(conversation_id, tool_message)
                    
                    # 继续下一轮
                    messages = self._get_conversation_history(conversation_id)
                    llm_messages = self._convert_messages_to_llm_format(messages)
                    continue
                else:
                    # 没有工具调用，返回最终答案
                    final_answer = "".join(collected_messages)
                    yield StreamChatResponse(
                        conversation_id=conversation_id,
                        content=final_answer,
                        is_final=True
                    )
                    break
            else:
                # 非流式处理
                response_content = response.choices[0].message.content
                tool_calls = response.choices[0].message.tool_calls
                
                if tool_calls:
                    # 执行工具调用
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)
                        result = await self._execute_tool_call(function_name, tool_args)
                        
                        # 更新对话历史
                        assistant_message = Message(
                            role=MessageRole.ASSISTANT,
                            content=None,
                            tool_calls=[{
                                "id": tool_call.id,
                                "type": "function",
                                "function": {
                                    "name": tool_call.function.name,
                                    "arguments": tool_call.function.arguments
                                }
                            }]
                        )
                        self._add_message_to_history(conversation_id, assistant_message)
                        
                        tool_message = Message(
                            role=MessageRole.TOOL,
                            name=function_name,
                            tool_call_id=tool_call.id,
                            content=str(result)
                        )
                        self._add_message_to_history(conversation_id, tool_message)
                    
                    # 继续下一轮
                    messages = self._get_conversation_history(conversation_id)
                    llm_messages = self._convert_messages_to_llm_format(messages)
                    continue
                else:
                    # 没有工具调用，返回最终答案
                    final_answer = response_content
                    break
        
        if not final_answer:
            final_answer = "未能理解您的问题"
        
        # 添加助手回复到历史
        assistant_message = Message(role=MessageRole.ASSISTANT, content=final_answer)
        self._add_message_to_history(conversation_id, assistant_message)
        
        if not stream:
            yield StreamChatResponse(
                conversation_id=conversation_id,
                content=final_answer,
                is_final=True
            )

    async def _get_available_tools_for_llm(self) -> List[Dict]:
        """
        获取LLM可用的工具列表
        
        Returns:
            List[Dict]: 工具列表
        """
        try:
            mcp_client = await self._get_mcp_client()
            tools = await mcp_client.list_tools()
            
            llm_tools = []
            for tool in tools:
                llm_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool["input_schema"]
                    }
                })
            
            return llm_tools
        except Exception as e:
            logger.error(f"获取工具列表失败: {e}")
            return []

    async def _execute_tool_call(self, function_name: str, tool_args: Dict) -> Any:
        """
        执行工具调用
        
        Args:
            function_name: 函数名称
            tool_args: 工具参数
            
        Returns:
            Any: 工具调用结果
        """
        try:
            mcp_client = await self._get_mcp_client()
            
            # 查找对应的服务器
            tools = await mcp_client.list_tools()
            server_name = None
            for tool in tools:
                if tool["name"] == function_name:
                    server_name = tool.get("server_name")
                    break
            
            if server_name is None:
                raise ValueError(f"未找到工具 {function_name} 对应的服务器")
            
            # 执行工具调用
            result = await mcp_client.call_tool(server_name, function_name, tool_args)
            
            # 提取结果文本
            if hasattr(result, 'content') and result.content:
                return result.content[0].text if result.content else ""
            else:
                return str(result)
                
        except Exception as e:
            logger.error(f"执行工具调用失败: {e}")
            return f"工具调用失败: {str(e)}"

    def _convert_messages_to_llm_format(self, messages: List[Message]) -> List[Dict]:
        """
        将消息转换为LLM格式
        
        Args:
            messages: 消息列表
            
        Returns:
            List[Dict]: LLM格式的消息列表
        """
        llm_messages = []
        for msg in messages:
            llm_msg = {
                "role": msg.role.value,
                "content": msg.content
            }
            
            if msg.tool_calls:
                llm_msg["tool_calls"] = msg.tool_calls
            
            if msg.tool_call_id:
                llm_msg["tool_call_id"] = msg.tool_call_id
            
            if msg.name:
                llm_msg["name"] = msg.name
            
            llm_messages.append(llm_msg)
        
        return llm_messages

    def get_conversation_history(self, conversation_id: str) -> List[Message]:
        """
        获取对话历史
        
        Args:
            conversation_id: 对话ID
            
        Returns:
            List[Message]: 对话历史
        """
        return self._get_conversation_history(conversation_id)

    def clear_conversation(self, conversation_id: str):
        """
        清除对话历史
        
        Args:
            conversation_id: 对话ID
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]

# 全局Agent实例
_agent_service: Optional[AgentService] = None

async def get_agent_service() -> AgentService:
    """获取全局Agent服务实例"""
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service 