from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.security import get_current_user
from app.models.user import User
from app.models.knowledge import Knowledge, KnowledgeChunk
from app.services.knowledge import embed_texts
from app.utils.milvus import search_vectors
from app.services.openai_client import generate_answer
from typing import List, Dict, Any
from loguru import logger

router = APIRouter()

class RAGQueryRequest(BaseModel):
    question: str
    knowledge_id: int
    top_k: int = 5

class RAGResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]

@router.post("/ask", response_model=RAGResponse)
async def rag_ask(
    data: RAGQueryRequest,
    current_user: User = Depends(get_current_user)
):
    """RAG问答接口"""
    try:
        # 1. 验证知识库是否存在
        knowledge = await Knowledge.filter(id=data.knowledge_id).first()
        if not knowledge:
            raise HTTPException(status_code=404, detail="知识库不存在")
        
        # 2. 问题向量化
        question_embedding = await embed_texts([data.question])
        if not question_embedding:
            raise HTTPException(status_code=500, detail="问题向量化失败")
        
        # 3. 向量检索
        search_results = await search_vectors(question_embedding[0], top_k=data.top_k)
        if not search_results:
            raise HTTPException(status_code=500, detail="向量检索失败")
        
        # 4. 获取相关文档片段
        vector_ids = [result.id for result in search_results[0]]
        chunks = await KnowledgeChunk.filter(
            knowledge_id=data.knowledge_id,
            vector_id__in=vector_ids
        ).all()
        
        # 5. 构建上下文
        context = "\n".join([chunk.content for chunk in chunks])
        
        # 6. 调用大模型生成答案
        prompt = f"""基于以下上下文回答问题：

上下文：
{context}

问题：{data.question}

请根据上下文提供准确、详细的答案。如果上下文中没有相关信息，请说明无法回答。"""
        
        answer = await generate_answer(prompt)
        
        # 7. 构建返回结果
        sources = []
        for chunk in chunks:
            sources.append({
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "vector_id": chunk.vector_id
            })
        
        return RAGResponse(answer=answer, sources=sources)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"RAG问答失败: {str(e)}")
        raise HTTPException(status_code=500, detail="RAG问答失败") 