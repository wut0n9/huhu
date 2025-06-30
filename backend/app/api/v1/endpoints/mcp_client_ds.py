#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This file provides a simple MCP client using just the mcp Python package.
It shows how to access the different MCP server capabilities (prompts, tools etc.) via the message types
supported by the protocol. See: https://modelcontextprotocol.io/docs/concepts/architecture.

Usage:
  python mcp_sse_client.py [--host HOSTNAME] [--port PORT]

Example:
  python mcp_sse_client.py --host ec2-44-192-72-20.compute-1.amazonaws.com --port 8000
"""
import argparse
from contextlib import AsyncExitStack
from mcp import types
from mcp import ClientSession
from mcp.client.sse import sse_client
import json
import asyncio

from openai import OpenAI



# deepseek
api_key = "sk-f308d35ee273467c8fa1adc9d1fec976"
model = "deepseek-reasoner"



class MCPClient:
    def __init__(self):
        """
        初始化MCP客户端
        
        Args:
            llm: LLM客户端实例
        """
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.service_sessions = {}  # 存储MCP服务名称与对应session的映射关系
        self.exit_stack = AsyncExitStack()
        self.running = True
        
    async def add_service_session(self, server_name: str, server_url: str):
        """
        添加新的服务会话
        
        Args:
            server_name: 服务名称
            server_url: MCP服务器URL
        """
        try:
            print(f"开始连接到服务 {server_name}，URL: {server_url}")
            
            # 创建SSE连接并管理其生命周期
            print("正在建立SSE连接...")

            stdio_transport = await self.exit_stack.enter_async_context(sse_client(server_url))
            print("SSE连接已建立，正在创建会话...")
            session = await self.exit_stack.enter_async_context(ClientSession(*stdio_transport, sampling_callback=handle_sampling_message))
            print("正在初始化会话...")
            await session.initialize()
            print("会话初始化成功")
            self.service_sessions[server_name] = session
            print(f"成功连接到服务: {server_name}")
            
        except Exception as e:
            print(f"连接服务 {server_name} 失败: {str(e)}")
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

    async def cleanup(self):
        """
        清理所有资源
        """
        self.running = False
        await self.exit_stack.aclose()

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

    async def get_service_session(self, server_name: str) -> ClientSession:
        """
        获取服务会话
        
        Args:
            server_name: 服务名称
            
        Returns:
            ClientSession: 服务会话实例
        """
        return self.service_sessions.get(server_name)

    async def list_available_services(self) -> list:
        """
        列出所有可用的服务名称
        
        Returns:
            list: 服务名称列表
        """
        return list(self.service_sessions.keys())

    async def process_query(self, query: str) -> str:
        """处理用户查询，支持多轮流式工具调用"""
        messages = [{"role": "user", "content": query}]
        final_answer = ""
        max_tool_rounds = 5  # 防止死循环

        # 预收集可用工具信息
        available_tools = []
        for server_name, session in self.service_sessions.items():
            tools_response = await session.list_tools()
            for tool in tools_response.tools:
                available_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })

        for round_idx in range(max_tool_rounds):
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=available_tools,
                tool_choice="auto",
                stream=True,
                temperature=0.1
            )

            collected_messages = []
            tool_call_accumulators = {}


            tool_call_id = None
            for chunk in response:
                delta = chunk.choices[0].delta

                # 收集普通内容
                if hasattr(delta, "content") and delta.content:
                    collected_messages.append(delta.content)
                    print(f"收到流式响应: {delta.content}")

                # 收集工具调用
                if hasattr(delta, "tool_calls") and delta.tool_calls:
                    for tool_call_delta in delta.tool_calls:
                        tool_call_id = tool_call_delta.id  if tool_call_delta.id else tool_call_id
                        if tool_call_id not in tool_call_accumulators:
                            tool_call_accumulators[tool_call_id] = {
                                "name": "",
                                "arguments": ""
                            }
                        if hasattr(tool_call_delta.function, "name") and tool_call_delta.function.name:
                            tool_call_accumulators[tool_call_id]["name"] = tool_call_delta.function.name
                        if hasattr(tool_call_delta.function, "arguments") and tool_call_delta.function.arguments:
                            tool_call_accumulators[tool_call_id]["arguments"] += tool_call_delta.function.arguments

            # 执行所有工具调用
            if tool_call_accumulators:
                for tool_call_id, tool_call in tool_call_accumulators.items():
                    function_name = tool_call["name"]
                    try:
                        tool_args = json.loads(tool_call["arguments"])
                    except Exception as e:
                        print(f"解析工具参数失败: {tool_call['arguments']}, 错误: {e}")
                        continue
                    session = self.service_sessions[function_name]
                    result = await session.call_tool(function_name, tool_args)
                    # 更新对话历史
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [{
                            "id": tool_call_id,
                            "type": "function",
                            "function": {
                                "name": function_name,
                                "arguments": json.dumps(tool_args, ensure_ascii=False)
                            }
                        }]
                    })
                    messages.append({
                        "role": "tool",
                        "name": function_name,
                        "tool_call_id": tool_call_id,
                        "content": result.content[0].text if result.content else ""
                    })
                # 继续下一轮
                continue
            else:
                # 没有工具调用，直接返回内容
                final_answer = "".join(collected_messages)
                break

        return final_answer if final_answer else "未能理解您的问题"


# Optional: create a sampling callback
async def handle_sampling_message(message: types.CreateMessageRequestParams) -> types.CreateMessageResult:
    """
    处理MCP服务器的采样消息
    
    Args:
        message: 包含服务器发送的采样消息参数
        
    Returns:
        CreateMessageResult: 标准化的响应格式
    """
    try:
        print(f"收到采样消息: {message}")
        # 处理中间生成结果
        if message.content and message.content.text:
            # 可以在这里添加自定义处理逻辑
            processed_text = message.content.text
            print(f"收到采样消息: {processed_text}")
            
            # 根据消息状态决定是否继续
            stop_reason = "endTurn" if message.is_final else "continue"
            print(f"消息状态: {stop_reason}")
            
            return types.CreateMessageResult(
                role="assistant",
                content=types.TextContent(
                    type="text",
                    text=processed_text,
                ),
                model=model,
                stopReason=stop_reason,
            )
        return None
    except Exception as e:
        print(f"处理采样消息时出错: {str(e)}")
        return None




async def run(server_url):
    print(f"Connecting to MCP server at: {server_url}")

    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            prompts = await session.list_prompts()
            print("=" * 50)
            print("Available prompts:")
            print("=" * 50)
            print(prompts)
            print("=" * 50)

            # List available resources
            # resources = await session.list_resources()
            # print("=" * 50)
            # print("Available resources:")
            # print("=" * 50)
            # print(resources)
            # print("=" * 50)

            # List available tools
            tools = await session.list_tools()
            print("=" * 50)
            print("Available tools:")
            print("=" * 50)
            print(tools)
            print("=" * 50)

            url = "https://www.modelscope.cn/learn"
            print(f"\nCalling tool 'fetch' with arguments:{url}")
            result = await session.call_tool(
                "fetch",
                arguments={"url": url, "raw": True}
            )

            # Display the results
            print("=" * 50)
            print("Fetch result:")
            print("=" * 50)
            for r in result.content:
                print(r.text)
            print("=" * 50)


async def main():
    max_retries = 3
    retry_count = 0
    
    try:
        while retry_count < max_retries:
            client = MCPClient()
            print(f"\n尝试连接 (第 {retry_count + 1} 次)...")
            await client.add_service_session(**server_config)
            
            fetch_url = "https://www.modelscope.cn/learn"
            print("正在处理查询...")
            result = await client.process_query(f"给我使用Fetch工具抓取以下网页原始内容并做文章总结：{fetch_url}")
            print(result)

            result = await client.process_query("你好，我是小明，请介绍一下你自己")
            print(result)
            

            break  # 如果成功，跳出循环
                
    finally:
        # 确保清理所有资源
        if client:
            await client.cleanup()

if __name__ == "__main__":

    server_config = {
            "server_name":"fetch",
            "server_url": "https://mcp.api-inference.modelscope.cn/sse/aa2a33e1bb644d"
    }
    # Run the async main function
    # asyncio.run(run(server_url))
    
    # 运行异步主函数
    asyncio.run(main())
