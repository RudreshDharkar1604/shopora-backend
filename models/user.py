from pydantic import BaseModel

class RegisterUserRequest(BaseModel):
    first_name: str
    last_name: str
    mobile_no:int
    email: str
    password: str
    address:str
    age : int 
    is_active: bool = True
    role: str = "user"

class LoginUserRequest(BaseModel):
    email: str
    password: str

