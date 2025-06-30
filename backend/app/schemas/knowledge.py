from pydantic import BaseModel
from typing import Optional

class KnowledgeBase(BaseModel):
    title: str
    content: str

class KnowledgeCreate(KnowledgeBase):
    pass

class KnowledgeOut(KnowledgeBase):
    id: int
    owner_id: int
    created_at: str
    class Config:
        orm_mode = True 