from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from app.schemas.knowledge import KnowledgeCreate, KnowledgeOut
from app.models.knowledge import Knowledge, KnowledgeChunk
from app.core.security import get_current_user
from app.models.user import User
from app.utils.minio import upload_file_to_minio, get_file_url
from app.services.knowledge import process_and_store_knowledge
from typing import List, Optional
from loguru import logger

router = APIRouter()

@router.post("/upload_file")
async def upload_knowledge_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传知识库文件"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="文件名不能为空")
        
        file_bytes = await file.read()
        object_name = upload_file_to_minio(file_bytes, file.filename)
        url = get_file_url(object_name)
        
        return {"object_name": object_name, "url": url}
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        raise HTTPException(status_code=500, detail="文件上传失败")

@router.post("/", response_model=KnowledgeOut)
async def create_knowledge(
    data: KnowledgeCreate,
    current_user: User = Depends(get_current_user)
):
    """创建知识库"""
    try:
        # 串联分词、嵌入、Milvus入库完整流程
        knowledge_id = await process_and_store_knowledge(
            data.title, 
            data.content, 
            owner_id=current_user.id
        )
        
        knowledge = await Knowledge.filter(id=knowledge_id).first()
        return KnowledgeOut(
            id=knowledge.id,
            title=knowledge.title,
            content=knowledge.content,
            owner_id=knowledge.owner_id,
            created_at=knowledge.created_at.isoformat()
        )
    except Exception as e:
        logger.error(f"创建知识库失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建知识库失败")

@router.get("/", response_model=List[KnowledgeOut])
async def list_knowledge(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    title: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
):
    """获取知识库列表"""
    try:
        query = Knowledge.all()
        
        # 按标题搜索
        if title:
            query = query.filter(title__icontains=title)
        
        # 分页
        total = await query.count()
        knowledge_list = await query.offset((page - 1) * size).limit(size)
        
        result = []
        for knowledge in knowledge_list:
            result.append(KnowledgeOut(
                id=knowledge.id,
                title=knowledge.title,
                content=knowledge.content,
                owner_id=knowledge.owner_id,
                created_at=knowledge.created_at.isoformat()
            ))
        
        return result
    except Exception as e:
        logger.error(f"获取知识库列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取知识库列表失败")

@router.get("/{knowledge_id}", response_model=KnowledgeOut)
async def get_knowledge(
    knowledge_id: int,
    current_user: User = Depends(get_current_user)
):
    """获取知识库详情"""
    try:
        knowledge = await Knowledge.filter(id=knowledge_id).first()
        if not knowledge:
            raise HTTPException(status_code=404, detail="知识库不存在")
        
        return KnowledgeOut(
            id=knowledge.id,
            title=knowledge.title,
            content=knowledge.content,
            owner_id=knowledge.owner_id,
            created_at=knowledge.created_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取知识库详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取知识库详情失败")

@router.get("/{knowledge_id}/chunks")
async def get_knowledge_chunks(
    knowledge_id: int,
    current_user: User = Depends(get_current_user)
):
    """获取知识库分片信息"""
    try:
        # 验证知识库是否存在
        knowledge = await Knowledge.filter(id=knowledge_id).first()
        if not knowledge:
            raise HTTPException(status_code=404, detail="知识库不存在")
        
        chunks = await KnowledgeChunk.filter(knowledge_id=knowledge_id).order_by('chunk_index').all()
        return [
            {
                "id": c.id,
                "chunk_index": c.chunk_index,
                "content": c.content,
                "vector_id": c.vector_id
            } for c in chunks
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取知识库分片失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取知识库分片失败")

@router.delete("/{knowledge_id}")
async def delete_knowledge(
    knowledge_id: int,
    current_user: User = Depends(get_current_user)
):
    """删除知识库"""
    try:
        knowledge = await Knowledge.filter(id=knowledge_id).first()
        if not knowledge:
            raise HTTPException(status_code=404, detail="知识库不存在")
        
        # 检查权限（只有创建者或管理员可以删除）
        roles = await current_user.get_roles()
        if knowledge.owner_id != current_user.id and "admin" not in roles:
            raise HTTPException(status_code=403, detail="权限不足")
        
        # 删除分片
        await KnowledgeChunk.filter(knowledge_id=knowledge_id).delete()
        
        # 删除知识库
        await knowledge.delete()
        
        return {"message": "知识库删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除知识库失败: {str(e)}")
        raise HTTPException(status_code=500, detail="删除知识库失败") 