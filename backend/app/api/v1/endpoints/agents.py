from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.user import User
from app.models.agent import Agent
from app.schemas.agent import Agent as AgentSchema, AgentCreate, AgentUpdate, AgentStatusUpdate
from app.services.user import user_service

router = APIRouter()


@router.get("/", response_model=List[AgentSchema])
async def read_agents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """获取用户的所有Agent"""
    result = await db.execute(
        select(Agent).where(Agent.user_id == current_user.id).offset(skip).limit(limit)
    )
    agents = result.scalars().all()
    return agents


@router.post("/", response_model=AgentSchema)
async def create_agent(
    *,
    db: AsyncSession = Depends(get_db),
    agent_in: AgentCreate,
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """创建新的Agent"""
    agent = Agent(
        **agent_in.dict(),
        user_id=current_user.id
    )
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent


@router.get("/{agent_id}", response_model=AgentSchema)
async def read_agent(
    *,
    db: AsyncSession = Depends(get_db),
    agent_id: int,
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """根据ID获取Agent"""
    result = await db.execute(
        select(Agent).where(Agent.id == agent_id, Agent.user_id == current_user.id)
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent不存在"
        )
    return agent


@router.put("/{agent_id}", response_model=AgentSchema)
async def update_agent(
    *,
    db: AsyncSession = Depends(get_db),
    agent_id: int,
    agent_in: AgentUpdate,
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """更新Agent"""
    result = await db.execute(
        select(Agent).where(Agent.id == agent_id, Agent.user_id == current_user.id)
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent不存在"
        )
    
    update_data = agent_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent


@router.patch("/{agent_id}/status", response_model=AgentSchema)
async def update_agent_status(
    *,
    db: AsyncSession = Depends(get_db),
    agent_id: int,
    status_update: AgentStatusUpdate,
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """更新Agent状态"""
    result = await db.execute(
        select(Agent).where(Agent.id == agent_id, Agent.user_id == current_user.id)
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent不存在"
        )
    
    agent.status = status_update.status
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent


@router.delete("/{agent_id}")
async def delete_agent(
    *,
    db: AsyncSession = Depends(get_db),
    agent_id: int,
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """删除Agent"""
    result = await db.execute(
        select(Agent).where(Agent.id == agent_id, Agent.user_id == current_user.id)
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent不存在"
        )
    
    await db.delete(agent)
    await db.commit()
    return {"message": "Agent删除成功"} 