# Milvus工具函数骨架
from typing import List, Dict
from pymilvus import Collection, connections
from app.core.config import settings

connections.connect(alias="default", host=settings.MILVUS_HOST, port=settings.MILVUS_PORT)
COLLECTION_NAME = "knowledge_chunk"

async def insert_vectors(vectors: List[List[float]], metadatas: List[Dict]) -> List[str]:
    collection = Collection(COLLECTION_NAME)
    # 假定schema: [id, vector, metadata]
    ids = [str(i) for i in range(len(vectors))]
    data = [ids, vectors, metadatas]
    mr = collection.insert(data)
    return mr.primary_keys

async def search_vectors(query_vector: List[float], top_k=5):
    collection = Collection(COLLECTION_NAME)
    results = collection.search([query_vector], "vector", search_params={"metric_type": "L2", "params": {"nprobe": 10}}, limit=top_k)
    return results 