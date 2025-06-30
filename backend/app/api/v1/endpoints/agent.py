from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
from app.services.agent_service import get_agent_service
from app.schemas.agent import ChatRequest, StreamChatResponse, MCPTool
from loguru import logger

router = APIRouter()

class MCPServerConfig(BaseModel):
    server_name: str
    server_url: str

class AddMCPServerRequest(BaseModel):
    server_name: str
    server_url: str

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Agent对话接口 - 流式响应
    """
    try:
        agent_service = await get_agent_service()
        
        # 如果有MCP服务器配置，先添加
        if request.mcp_servers:
            for server_config in request.mcp_servers:
                try:
                    await agent_service.add_mcp_server(
                        server_config["server_name"], 
                        server_config["server_url"]
                    )
                except Exception as e:
                    logger.warning(f"添加MCP服务器失败: {e}")
        
        async def generate_stream():
            async for response in agent_service.process_query(
                query=request.message,
                conversation_id=request.conversation_id,
                stream=True
            ):
                yield f"data: {json.dumps(response.model_dump(), ensure_ascii=False)}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        logger.error(f"Agent对话失败: {e}")
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")

@router.post("/mcp/servers")
async def add_mcp_server(request: AddMCPServerRequest):
    """
    添加MCP服务器
    """
    try:
        agent_service = await get_agent_service()
        await agent_service.add_mcp_server(request.server_name, request.server_url)
        return {"message": f"成功添加MCP服务器: {request.server_name}"}
    except Exception as e:
        logger.error(f"添加MCP服务器失败: {e}")
        raise HTTPException(status_code=500, detail=f"添加MCP服务器失败: {str(e)}")

@router.delete("/mcp/servers/{server_name}")
async def remove_mcp_server(server_name: str):
    """
    移除MCP服务器
    """
    try:
        agent_service = await get_agent_service()
        await agent_service.remove_mcp_server(server_name)
        return {"message": f"成功移除MCP服务器: {server_name}"}
    except Exception as e:
        logger.error(f"移除MCP服务器失败: {e}")
        raise HTTPException(status_code=500, detail=f"移除MCP服务器失败: {str(e)}")

@router.get("/mcp/servers")
async def list_mcp_servers():
    """
    列出所有MCP服务器
    """
    try:
        agent_service = await get_agent_service()
        servers = await agent_service.list_mcp_servers()
        return {"servers": servers}
    except Exception as e:
        logger.error(f"获取MCP服务器列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取MCP服务器列表失败: {str(e)}")

@router.get("/mcp/tools")
async def list_mcp_tools():
    """
    列出所有可用工具
    """
    try:
        agent_service = await get_agent_service()
        tools = await agent_service.list_available_tools()
        return {"tools": tools}
    except Exception as e:
        logger.error(f"获取工具列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取工具列表失败: {str(e)}")

@router.get("/conversations/{conversation_id}/history")
async def get_conversation_history(conversation_id: str):
    """
    获取对话历史
    """
    try:
        agent_service = await get_agent_service()
        history = agent_service.get_conversation_history(conversation_id)
        return {"conversation_id": conversation_id, "history": history}
    except Exception as e:
        logger.error(f"获取对话历史失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取对话历史失败: {str(e)}")

@router.delete("/conversations/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """
    清除对话历史
    """
    try:
        agent_service = await get_agent_service()
        agent_service.clear_conversation(conversation_id)
        return {"message": f"成功清除对话: {conversation_id}"}
    except Exception as e:
        logger.error(f"清除对话失败: {e}")
        raise HTTPException(status_code=500, detail=f"清除对话失败: {str(e)}") 