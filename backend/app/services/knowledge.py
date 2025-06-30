# 知识库相关业务逻辑
from typing import List
import httpx
from app.core.config import settings
from loguru import logger

async def split_text(text: str) -> List[str]:
    """文本分块"""
    # 简单按段落分割
    chunks = [chunk.strip() for chunk in text.split("\n") if chunk.strip()]
    # 如果单个块太长，进一步分割
    result = []
    for chunk in chunks:
        if len(chunk) > 1000:
            # 按句号分割
            sentences = chunk.split('。')
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk + sentence) > 1000:
                    if current_chunk:
                        result.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk += sentence + "。"
            if current_chunk:
                result.append(current_chunk.strip())
        else:
            result.append(chunk)
    return result

async def embed_texts(texts: List[str]) -> List[List[float]]:
    """文本向量化"""
    try:
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API Key未配置，返回随机向量")
            import random
            return [[random.random() for _ in range(1536)] for _ in texts]
        
        url = f"{settings.OPENAI_BASE_URL}/embeddings"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "input": texts,
            "model": settings.OPENAI_EMBEDDING_MODEL
        }
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return [item["embedding"] for item in data["data"]]
    except Exception as e:
        logger.error(f"文本向量化失败: {str(e)}")
        # 返回随机向量作为fallback
        import random
        return [[random.random() for _ in range(1536)] for _ in texts]

async def process_and_store_knowledge(title: str, content: str, owner_id: int):
    """处理并存储知识库"""
    try:
        from app.models.knowledge import Knowledge, KnowledgeChunk
        from app.utils.milvus import insert_vectors
        
        # 1. 分词
        chunks = await split_text(content)
        if not chunks:
            raise ValueError("文本内容为空或无法分割")
        
        # 2. 嵌入
        vectors = await embed_texts(chunks)
        if not vectors:
            raise ValueError("向量化失败")
        
        # 3. Milvus入库
        metadatas = [{"title": title, "chunk_index": i} for i in range(len(chunks))]
        vector_ids = await insert_vectors(vectors, metadatas)
        if not vector_ids:
            raise ValueError("向量存储失败")
        
        # 4. 数据库记录
        knowledge = await Knowledge.create(title=title, content=content, owner_id=owner_id)
        
        # 5. 存储分片信息
        for i, (chunk, vector_id) in enumerate(zip(chunks, vector_ids)):
            await KnowledgeChunk.create(
                knowledge=knowledge, 
                chunk_index=i, 
                content=chunk, 
                vector_id=str(vector_id)
            )
        
        logger.info(f"知识库处理完成: {title}, 分片数: {len(chunks)}")
        return knowledge.id
        
    except Exception as e:
        logger.error(f"知识库处理失败: {str(e)}")
        raise 