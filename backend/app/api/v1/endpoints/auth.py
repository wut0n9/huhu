from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.user import register_user, authenticate_user, create_jwt_for_user
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserOut
from loguru import logger

router = APIRouter()

class UserRegisterRequest(BaseModel):
    username: str
    password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

@router.post("/register")
async def register(data: UserRegisterRequest):
    """用户注册"""
    try:
        user = await register_user(data.username, data.password)
        return {"msg": "注册成功", "user_id": user.id}
    except Exception as e:
        logger.error(f"用户注册失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=LoginResponse)
async def login(data: UserLoginRequest):
    """用户登录"""
    try:
        user = await authenticate_user(data.username, data.password)
        if not user:
            raise HTTPException(status_code=401, detail="用户名或密码错误")
        
        token = await create_jwt_for_user(user)
        roles = await user.get_roles()
        
        return LoginResponse(
            access_token=token,
            token_type="bearer",
            user=UserOut(
                id=user.id,
                username=user.username,
                is_active=user.is_active,
                roles=roles
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"用户登录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="登录失败")

@router.get("/me")
async def me(user=Depends(get_current_user)):
    return {"id": user.id, "username": user.username, "roles": user.roles} 