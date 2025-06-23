from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.conversation import MessageRole, ConversationStatus


class MessageBase(BaseModel):
    """消息基础模式"""
    role: MessageRole
    content: str = Field(..., min_length=1)


class MessageCreate(MessageBase):
    """创建消息模式"""
    pass


class MessageInDB(MessageBase):
    """数据库中的消息模式"""
    id: int
    conversation_id: int
    metadata: Optional[dict] = None
    tokens_used: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Message(MessageInDB):
    """消息响应模式"""
    pass


class ConversationBase(BaseModel):
    """对话基础模式"""
    title: Optional[str] = Field(None, max_length=200)
    status: ConversationStatus = ConversationStatus.ACTIVE


class ConversationCreate(ConversationBase):
    """创建对话模式"""
    agent_id: int


class ConversationUpdate(BaseModel):
    """更新对话模式"""
    title: Optional[str] = Field(None, max_length=200)
    status: Optional[ConversationStatus] = None


class ConversationInDB(ConversationBase):
    """数据库中的对话模式"""
    id: int
    user_id: int
    agent_id: int
    message_count: int
    total_tokens: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Conversation(ConversationInDB):
    """对话响应模式"""
    pass


class ConversationWithMessages(Conversation):
    """包含消息的对话响应模式"""
    messages: List[Message] = []


class ChatRequest(BaseModel):
    """聊天请求模式"""
    message: str = Field(..., min_length=1, description="用户消息")
    conversation_id: Optional[int] = None
    agent_id: int = Field(..., description="Agent ID")


class ChatResponse(BaseModel):
    """聊天响应模式"""
    message: Message
    conversation_id: int
    tokens_used: int
    response_time: float 