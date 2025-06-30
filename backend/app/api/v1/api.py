from fastapi import APIRouter
from .endpoints import auth, users, roles, knowledge, rag, mcp, text2sql, chatbi, visualization, agent

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(roles.router, prefix="/roles", tags=["roles"])
router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
router.include_router(rag.router, prefix="/rag", tags=["rag"])
router.include_router(mcp.router, prefix="/mcp", tags=["mcp"])
router.include_router(text2sql.router, prefix="/text2sql", tags=["text2sql"])
router.include_router(chatbi.router, prefix="/chatbi", tags=["chatbi"])
router.include_router(visualization.router, prefix="/visualization", tags=["visualization"])
router.include_router(agent.router, prefix="/agent", tags=["agent"])

# 后续各功能模块路由在此引入并挂载 