import httpx
from app.core.config import settings
from loguru import logger

async def generate_answer(prompt: str) -> str:
    """调用OpenAI API生成答案"""
    try:
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API Key未配置，返回默认答案")
            return "抱歉，AI服务暂时不可用，请检查配置。"
        
        url = f"{settings.OPENAI_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": settings.OPENAI_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenAI API返回异常: {data}")
                return "抱歉，AI生成答案时出现错误。"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenAI API HTTP错误: {e.response.status_code} - {e.response.text}")
        return "抱歉，AI服务暂时不可用。"
    except Exception as e:
        logger.error(f"调用OpenAI API失败: {str(e)}")
        return "抱歉，AI服务暂时不可用。"

async def generate_sql(question: str, schema: str) -> str:
    """调用OpenAI API生成SQL"""
    try:
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API Key未配置，返回默认SQL")
            return "SELECT 1"
        
        url = f"{settings.OPENAI_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""你是一个SQL专家，请根据以下数据库结构和问题生成SQL查询语句。

数据库结构：
{schema}

问题：{question}

请只返回SQL语句，不要包含其他解释。"""
        
        payload = {
            "model": settings.OPENAI_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.1
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"].strip()
            else:
                logger.error(f"OpenAI API返回异常: {data}")
                return "SELECT 1"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenAI API HTTP错误: {e.response.status_code} - {e.response.text}")
        return "SELECT 1"
    except Exception as e:
        logger.error(f"调用OpenAI API失败: {str(e)}")
        return "SELECT 1" 