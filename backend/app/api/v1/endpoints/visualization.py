from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict
import pymysql
from app.core.config import settings

router = APIRouter()

class VisualizationRequest(BaseModel):
    db_url: str
    chart_type: str  # e.g. bar, line, pie
    sql: str

@router.post("/data")
async def get_visualization_data(data: VisualizationRequest):
    # 真实执行SQL，返回ECharts可用数据结构
    import re
    m = re.match(r"mysql://(.*?):(.*?)@(.*?):(\d+)/(.*?)$", data.db_url)
    if not m:
        return {"error": "db_url格式错误"}
    user, pwd, host, port, db = m.groups()
    conn = pymysql.connect(host=host, port=int(port), user=user, password=pwd, database=db, charset='utf8mb4')
    try:
        with conn.cursor() as cursor:
            cursor.execute(data.sql)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            # ECharts数据结构转换
            return {
                "columns": columns,
                "rows": [list(row) for row in rows],
                "chart_type": data.chart_type
            }
    finally:
        conn.close() 