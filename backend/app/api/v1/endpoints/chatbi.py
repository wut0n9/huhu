from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Any
from app.services.text2sql import nl_to_sql, exec_sql
from app.core.security import get_current_user
from app.models.user import User
import pymysql
from loguru import logger

router = APIRouter()

class ChatBIMessage(BaseModel):
    role: str  # user/assistant
    content: str

class ChatBIRequest(BaseModel):
    messages: List[ChatBIMessage]
    db_url: str

class ChatBIResponse(BaseModel):
    answer: str
    sql: str
    result: List[Any]

async def get_db_schema(db_url: str) -> str:
    """获取数据库结构"""
    try:
        import re
        m = re.match(r"mysql://(.*?):(.*?)@(.*?):(\d+)/(.*?)$", db_url)
        if not m:
            raise ValueError("db_url格式错误")
        
        user, pwd, host, port, db = m.groups()
        conn = pymysql.connect(
            host=host, 
            port=int(port), 
            user=user, 
            password=pwd, 
            database=db, 
            charset='utf8mb4'
        )
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]
                schema = []
                for t in tables:
                    cursor.execute(f"SHOW CREATE TABLE `{t}`")
                    schema.append(cursor.fetchone()[1])
                return "\n".join(schema)
        finally:
            conn.close()
    except Exception as e:
        logger.error(f"获取数据库结构失败: {str(e)}")
        return ""

@router.post("/chat", response_model=ChatBIResponse)
async def chat_bi(
    data: ChatBIRequest,
    current_user: User = Depends(get_current_user)
):
    """ChatBI对话接口"""
    try:
        # 获取数据库结构
        db_schema = await get_db_schema(data.db_url)
        if not db_schema:
            raise HTTPException(status_code=400, detail="无法获取数据库结构")
        
        # 只取最后一轮用户问题生成SQL
        if not data.messages:
            raise HTTPException(status_code=400, detail="消息不能为空")
        
        question = data.messages[-1].content if data.messages else ""
        if not question:
            raise HTTPException(status_code=400, detail="问题不能为空")
        
        # 生成SQL
        sql = await nl_to_sql(question, db_schema)
        if not sql:
            raise HTTPException(status_code=500, detail="SQL生成失败")
        
        # 执行SQL
        result = await exec_sql(data.db_url, sql)
        
        # 生成回答
        answer = f"根据您的问题，我生成了以下SQL查询：\n\n```sql\n{sql}\n```\n\n查询结果共{len(result)}条记录。"
        
        return ChatBIResponse(
            answer=answer,
            sql=sql,
            result=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ChatBI对话失败: {str(e)}")
        raise HTTPException(status_code=500, detail="ChatBI对话失败") 