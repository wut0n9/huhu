from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.agent import AgentStatus, AgentType


class AgentBase(BaseModel):
    """Agent基础模式"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    agent_type: AgentType = AgentType.CHAT
    system_prompt: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class AgentCreate(AgentBase):
    """创建Agent模式"""
    model_config: Dict[str, Any] = Field(..., description="模型配置")


class AgentUpdate(BaseModel):
    """更新Agent模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    agent_type: Optional[AgentType] = None
    system_prompt: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    model_config: Optional[Dict[str, Any]] = None


class AgentInDB(AgentBase):
    """数据库中的Agent模式"""
    id: int
    status: AgentStatus
    user_id: int
    model_config: Dict[str, Any]
    total_conversations: int
    total_tokens_used: int
    last_activity: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Agent(AgentInDB):
    """Agent响应模式"""
    pass


class AgentStatusUpdate(BaseModel):
    """Agent状态更新模式"""
    status: AgentStatus


class AgentConfig(BaseModel):
    """Agent配置模式"""
    model_name: str = Field(..., description="模型名称")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="温度参数")
    max_tokens: int = Field(1000, ge=1, le=4000, description="最大token数")
    top_p: float = Field(1.0, ge=0.0, le=1.0, description="Top-p参数")
    frequency_penalty: float = Field(0.0, ge=-2.0, le=2.0, description="频率惩罚")
    presence_penalty: float = Field(0.0, ge=-2.0, le=2.0, description="存在惩罚") 