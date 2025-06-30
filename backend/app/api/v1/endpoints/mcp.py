from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from app.services.mcp_client import get_mcp_client
import json

router = APIRouter()

class ToolCallRequest(BaseModel):
    tool_name: str
    tool_args: Dict[str, Any]
    server_script_path: str

@router.post("/list_tools")
async def list_tools(server_script_path: str = Query(..., description="MCP Server脚本路径")):
    try:
        client = await get_mcp_client(server_script_path)
        tools = await client.list_tools()
        return {"tools": tools}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工具列表失败: {str(e)}")

@router.post("/call_tool")
async def call_tool(req: ToolCallRequest):
    try:
        client = await get_mcp_client(req.server_script_path)
        result = await client.call_tool(req.tool_name, req.tool_args)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"工具调用失败: {str(e)}")

@router.get("/servers")
async def list_servers():
    """获取可用的MCP Server列表"""
    # 这里可以从配置文件或数据库读取
    return {
        "servers": [
            {"name": "示例Server", "path": "/path/to/server.py", "description": "示例MCP Server"}
        ]
    } 