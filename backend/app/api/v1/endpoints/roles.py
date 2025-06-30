from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.models.user import User
from app.models.role import Role
from app.schemas.role import RoleOut, RoleBase
from typing import List
from loguru import logger

router = APIRouter()

@router.get("/", response_model=List[RoleOut])
async def list_roles(current_user: User = Depends(get_current_user)):
    """获取所有角色列表"""
    try:
        roles = await Role.all()
        return [RoleOut(id=role.id, name=role.name, description=role.description) for role in roles]
    except Exception as e:
        logger.error(f"获取角色列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取角色列表失败")

@router.post("/", response_model=RoleOut)
async def create_role(
    role_data: RoleBase,
    current_user: User = Depends(get_current_user)
):
    """创建新角色（需要管理员权限）"""
    try:
        # 检查权限
        roles = await current_user.get_roles()
        if "admin" not in roles:
            raise HTTPException(status_code=403, detail="权限不足")
        
        # 检查角色名是否已存在
        existing_role = await Role.filter(name=role_data.name).first()
        if existing_role:
            raise HTTPException(status_code=400, detail="角色名已存在")
        
        # 创建新角色
        role = await Role.create(
            name=role_data.name,
            description=role_data.description
        )
        
        return RoleOut(id=role.id, name=role.name, description=role.description)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建角色失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建角色失败")

@router.get("/{role_id}", response_model=RoleOut)
async def get_role(
    role_id: int,
    current_user: User = Depends(get_current_user)
):
    """获取角色详情"""
    try:
        role = await Role.filter(id=role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail="角色不存在")
        
        return RoleOut(id=role.id, name=role.name, description=role.description)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取角色详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取角色详情失败") 