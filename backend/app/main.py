import os
from dotenv import load_dotenv

# 首先加载环境变量，必须在导入settings之前
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.v1.api import router as api_v1_router
from app.core.database import init_db, close_db
from app.services.mcp_client import close_mcp_client
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.middleware.logging import LoggingMiddleware
import sys

# 初始化日志系统
setup_logging()
logger = get_logger(__name__)

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

# 添加日志中间件，配置流式响应路径
app.add_middleware(
    LoggingMiddleware,
    streaming_paths=["/api/v1/agent/chat"],  # 流式响应路径不读取request body
    enabled=settings.DEBUG or True  # 可以根据环境配置启用/禁用
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
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
