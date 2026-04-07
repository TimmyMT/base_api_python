from pydantic import BaseModel

# ----------------- SCHEMAS -----------------

class RoleAssignRequest(BaseModel):
    user_id: int
    role_id: int

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    name: str

class RoleUpdate(RoleBase):
    name: str

class RoleResponse(RoleBase):
    id: int
    name: str

    class Config:
        orm_mode = True
