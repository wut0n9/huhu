from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.v1.api import router as api_v1_router
from app.core.database import init_db, close_db
from app.services.mcp_client import close_mcp_client
from app.core.config import settings
from loguru import logger
import sys

# 配置日志
logger.remove()
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level=settings.LOG_LEVEL
)
logger.add(
    "logs/app.log",
    rotation="1 day",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level=settings.LOG_LEVEL
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动事件
    logger.info("应用启动中...")
    await init_db()
    logger.info("应用启动完成")
    
    yield
    
    # 关闭事件
    logger.info("应用关闭中...")
    await close_db()
    await close_mcp_client()
    logger.info("应用关闭完成")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="RAG问答、数据可视化、ChatBI、MCP工具、Text2SQL平台",
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"全局异常: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误"}
    )

# 健康检查
@app.get("/ping")
def ping():
    return {"msg": "pong", "status": "healthy"}

# 包含API路由
app.include_router(api_v1_router, prefix="/api/v1")

# 路由将在api目录下分模块引入
