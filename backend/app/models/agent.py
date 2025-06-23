from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class AgentStatus(str, enum.Enum):
    """Agent状态枚举"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    STOPPED = "stopped"


class AgentType(str, enum.Enum):
    """Agent类型枚举"""
    CHAT = "chat"
    TASK = "task"
    WORKFLOW = "workflow"
    CUSTOM = "custom"


class Agent(Base):
    """Agent模型"""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    agent_type = Column(Enum(AgentType), default=AgentType.CHAT)
    status = Column(Enum(AgentStatus), default=AgentStatus.IDLE)
    
    # 配置信息
    model_config = Column(JSON, nullable=False)  # 模型配置
    system_prompt = Column(Text, nullable=True)  # 系统提示词
    parameters = Column(JSON, nullable=True)  # 运行参数
    
    # 关联信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by = relationship("User", backref="agents")
    
    # 统计信息
    total_conversations = Column(Integer, default=0)
    total_tokens_used = Column(Integer, default=0)
    last_activity = Column(DateTime(timezone=True), nullable=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Agent(id={self.id}, name='{self.name}', status='{self.status}')>" 