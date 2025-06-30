from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserOut
from typing import List
from loguru import logger

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    try:
        roles = await current_user.get_roles()
        return UserOut(
            id=current_user.id,
            username=current_user.username,
            is_active=current_user.is_active,
            roles=roles
        )
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取用户信息失败")

@router.get("/", response_model=List[UserOut])
async def list_users(
    page: int = 1,
    size: int = 10,
    current_user: User = Depends(get_current_user)
):
    """获取用户列表（需要管理员权限）"""
    try:
        # 检查权限
        roles = await current_user.get_roles()
        if "admin" not in roles:
            raise HTTPException(status_code=403, detail="权限不足")
        
        # 分页查询
        offset = (page - 1) * size
        users = await User.all().offset(offset).limit(size)
        
        result = []
        for user in users:
            roles = await user.get_roles()
            result.append(UserOut(
                id=user.id,
                username=user.username,
                is_active=user.is_active,
                roles=roles
            ))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取用户列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取用户列表失败") 