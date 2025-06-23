from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, agents, conversations

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agent管理"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["对话管理"]) 