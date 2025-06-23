from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate
from app.services.user import user_service

router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """获取当前用户信息"""
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(user_service.get_current_user),
) -> Any:
    """更新当前用户信息"""
    user = await user_service.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=UserSchema)
async def read_user_by_id(
    user_id: int,
    current_user: User = Depends(user_service.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """根据ID获取用户"""
    user = await user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400,
            detail="权限不足"
        )
    return user 