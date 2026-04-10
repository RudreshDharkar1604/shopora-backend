from datetime import timedelta

from fastapi import APIRouter, Depends
from utlis.jwt_token import create_access_token
from core.config import settings
from core.security import hash_password,verify_password
from db.database import AsyncSession, get_db
from models.user import RegisterUserRequest, LoginUserRequest
from psycopg.auth import check_user_exists, login_controller, register_user
from exceptions.user_exceptions import UserNotFoundException

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

@router.post("/register")
async def register(request: RegisterUserRequest, db: AsyncSession = Depends(get_db)):
    try:
        if await check_user_exists(request.email, request.mobile_no, db):
            return {"error": "User with this email or mobile number already exists"}
        
        result = await register_user(
            first_name=request.first_name, last_name=request.last_name, mobile_no=request.mobile_no,
            email=request.email, password=request.password, address=request.address, age=request.age, 
            is_active=request.is_active, role=request.role, db=db)
        return result
    except Exception as e:
        return {"error": str(e)}
    

@router.post("/login")
async def login(request: LoginUserRequest, db: AsyncSession = Depends(get_db)):
    try:
        if not request.email or not request.password:
            return {"error": "Email and password are required"}
        user = await check_user_exists(request.email, None, db)
        stored_password = user['password'] if user else None
        if not user:
            print("User not found ")
            raise UserNotFoundException(userDetails=request.email)
        if not verify_password(request.password, stored_password):
            return {"error": "Invalid password"}
        result = await login_controller(request.email, stored_password, db)
        print("Login Result:", result)  
        if not result:
            return {"error": "Invalid email or password"}
        token = await create_access_token(data={"sub":result}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise e