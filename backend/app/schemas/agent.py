from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    SYSTEM = "system"

class ToolCall(BaseModel):
    id: str
    type: str = "function"
    function: Dict[str, Any]

class Message(BaseModel):
    role: MessageRole
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None

class ChatRequest(BaseModel):
    message: str = Field(..., description="用户消息")
    conversation_id: Optional[str] = Field(None, description="对话ID")
    stream: bool = Field(False, description="是否使用流式响应")
    mcp_servers: Optional[List[Dict[str, str]]] = Field(None, description="MCP服务器配置列表")

class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    usage: Optional[Dict[str, Any]] = None

class StreamChatResponse(BaseModel):
    conversation_id: str
    content: str
    is_final: bool = False
    tool_calls: Optional[List[Dict[str, Any]]] = None

class MCPTool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]

class MCPToolCall(BaseModel):
    tool_name: str
    tool_args: Dict[str, Any]
    server_name: str

class AgentConfig(BaseModel):
    model: str
    temperature: float = 0.1
    max_tool_rounds: int = 5
    max_history: int = 10 