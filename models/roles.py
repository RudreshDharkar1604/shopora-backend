from pydantic import BaseModel

class CreateRolesRequest(BaseModel):
    role_name:str
    role_description: str = None
