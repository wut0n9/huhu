# Milvus工具函数骨架
from typing import List, Dict
from pymilvus import Collection, connections
from app.core.config import settings

MILVUS_URI="https://in03-ea9f450d4e523c2.serverless.gcp-us-west1.cloud.zilliz.com"
MILVUS_TOKEN="807bed4ee781aa7ca88c7c3891a5b991d1da3bd42b3355b55f2a632e6a810237e70cb71b1b3341126ca88abe3ab21cd0abcd2c5d"

connections.connect(alias="default", uri=MILVUS_URI, token=MILVUS_TOKEN)
COLLECTION_NAME = "knowledge_chunk"

