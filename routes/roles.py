from fastapi import APIRouter,Depends

from db.database import get_db,AsyncDatabase
from psycopg.roles import get_all_roles
from fastapi import Request
from models.roles import CreateRolesRequest
from exceptions.permissions_exception import InvalidAccessException
from psycopg.roles import create_a_new_role
from utlis.swagger_token_verify import verify_swagger_token

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/")
async def get_roles(db:AsyncDatabase = Depends(get_db)):
    try:
        roles = await get_all_roles(db)
        return roles
    except Exception as e:
        return {"error" : str(e)}

@router.post("/")
async def create_role(request : CreateRolesRequest ,token = Depends(verify_swagger_token), db : AsyncDatabase = Depends(get_db)):
    try:
        # if request.state.role != 'admin':
        #     print("user role is ",request.state.role)
        #     raise InvalidAccessException(user_role=request.state.role)
        result = await create_a_new_role(role_name=request.role_name,role_description=request.role_description,db=db)
        return result
    except Exception as e:
        return {"error" : str(e)}