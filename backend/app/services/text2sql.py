# Text2SQL服务
import pymysql
from app.services.openai_client import generate_sql
from loguru import logger
from typing import List, Any

async def nl_to_sql(question: str, db_schema: str) -> str:
    """自然语言转SQL"""
    try:
        sql = await generate_sql(question, db_schema)
        return sql
    except Exception as e:
        logger.error(f"自然语言转SQL失败: {str(e)}")
        return "SELECT 1"

async def exec_sql(db_url: str, sql: str) -> List[Any]:
    """执行SQL查询"""
    try:
        # 仅支持mysql://user:pwd@host:port/db格式
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
                cursor.execute(sql)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]
        finally:
            conn.close()
    except Exception as e:
        logger.error(f"SQL执行失败: {str(e)}")
        raise 