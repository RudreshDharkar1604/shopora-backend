from pydantic import BaseModel

class RegisterUserRequest(BaseModel):
    first_name: str
    last_name: str
    mobile_number:int
    email: str
    password: str
    address:str
    age : int 
    is_active: bool = True
    role: int = 1  

class LoginUserRequest(BaseModel):
    email: str
    password: str

class UpdateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email:str = None
    role: str = None
    mobile_number:int
    address:str
    age : int

