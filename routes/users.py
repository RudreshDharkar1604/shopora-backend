from fastapi import APIRouter, Depends
from db.database import AsyncSession, get_db    
from models.user import UpdateUserRequest
from psycopg.user import get_user_details_by_id, update_user_by_id


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
async def get_user_details(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        user_details = await get_user_details_by_id(user_id, db)
        if not user_details:
            return {"error": "User not found"}
        return user_details
    except Exception as e:
        return {"error": str(e)}
    

@router.put("/{user_id}")
async def update_user_details_by_id(user_id: int, req: UpdateUserRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await update_user_by_id(user_id, req.first_name, req.last_name, req.mobile_number, req.email, req.address, req.age, db)
        return result
    except Exception as e:
        return {"error": str(e)}