from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.schemas.conversation import (
    Conversation as ConversationSchema,
    ConversationCreate,
    ConversationUpdate,
    ConversationWithMessages,
    Message as MessageSchema,
    ChatRequest,
    ChatResponse
)
from app.services.user import user_service

router = APIRouter()


@router.get("/", response_model=List[ConversationSchema])
async def read_conversations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """获取用户的所有对话"""
    result = await db.execute(
        select(Conversation).where(Conversation.user_id == current_user.id).offset(skip).limit(limit)
    )
    conversations = result.scalars().all()
    return conversations


@router.post("/", response_model=ConversationSchema)
async def create_conversation(
    *,
    db: AsyncSession = Depends(get_db),
    conversation_in: ConversationCreate,
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """创建新的对话"""
    conversation = Conversation(
        **conversation_in.dict(),
        user_id=current_user.id
    )
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation


@router.get("/{conversation_id}", response_model=ConversationWithMessages)
async def read_conversation(
    *,
    db: AsyncSession = Depends(get_db),
    conversation_id: int,
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """根据ID获取对话及其消息"""
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="对话不存在"
        )
    return conversation


@router.put("/{conversation_id}", response_model=ConversationSchema)
async def update_conversation(
    *,
    db: AsyncSession = Depends(get_db),
    conversation_id: int,
    conversation_in: ConversationUpdate,
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """更新对话"""
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="对话不存在"
        )
    
    update_data = conversation_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(conversation, field, value)
    
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation


@router.delete("/{conversation_id}")
async def delete_conversation(
    *,
    db: AsyncSession = Depends(get_db),
    conversation_id: int,
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """删除对话"""
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="对话不存在"
        )
    
    await db.delete(conversation)
    await db.commit()
    return {"message": "对话删除成功"}


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    *,
    db: AsyncSession = Depends(get_db),
    chat_request: ChatRequest,
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """与Agent聊天"""
    import time
    start_time = time.time()
    
    # 这里应该实现实际的聊天逻辑
    # 暂时返回模拟响应
    response_time = time.time() - start_time
    
    # 创建或获取对话
    if chat_request.conversation_id:
        result = await db.execute(
            select(Conversation).where(
                Conversation.id == chat_request.conversation_id,
                Conversation.user_id == current_user.id
            )
        )
        conversation = result.scalar_one_or_none()
        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="对话不存在"
            )
    else:
        # 创建新对话
        conversation = Conversation(
            user_id=current_user.id,
            agent_id=chat_request.agent_id,
            title=chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
    
    # 创建用户消息
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=chat_request.message
    )
    db.add(user_message)
    
    # 创建助手消息（模拟）
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=f"这是对'{chat_request.message}'的回复。",
        tokens_used=100
    )
    db.add(assistant_message)
    
    # 更新对话统计
    conversation.message_count += 2
    conversation.total_tokens += 100
    
    await db.commit()
    await db.refresh(assistant_message)
    
    return ChatResponse(
        message=assistant_message,
        conversation_id=conversation.id,
        tokens_used=100,
        response_time=response_time
    ) 