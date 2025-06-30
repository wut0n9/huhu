from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict
from app.services.text2sql import nl_to_sql, exec_sql
import pymysql

router = APIRouter()

class Text2SQLRequest(BaseModel):
    question: str
    db_url: str

async def get_db_schema(db_url: str) -> str:
    # 连接数据库获取所有表结构
    import re
    m = re.match(r"mysql://(.*?):(.*?)@(.*?):(\d+)/(.*?)$", db_url)
    if not m:
        return ""
    user, pwd, host, port, db = m.groups()
    conn = pymysql.connect(host=host, port=int(port), user=user, password=pwd, database=db, charset='utf8mb4')
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

@router.post("/query")
async def text2sql_query(data: Text2SQLRequest):
    db_schema = await get_db_schema(data.db_url)
    sql = await nl_to_sql(data.question, db_schema)
    result = await exec_sql(data.db_url, sql)
    return {
        "sql": sql,
        "result": result
    } 