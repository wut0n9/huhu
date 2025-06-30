from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str
    description: str = ""

class RoleOut(RoleBase):
    id: int
    class Config:
        orm_mode = True 