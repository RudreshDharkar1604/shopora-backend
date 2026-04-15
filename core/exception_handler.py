from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.user_exceptions import UserNotFoundException
from exceptions.permissions_exception import InvalidAccessException

async def app_exception_handler(request, exc: BaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message
        }
    )

async def user_not_found_exception_handler(request , exc : UserNotFoundException):
    return JSONResponse(
        status_code=exc.status_code | 404,
        content=exc.message | exc.details 
    )

async def invalid_permission_exception_handler(request , exc: InvalidAccessException):
    return JSONResponse(
        status_code=exc.status_code | 404,
        content=exc.message | exc.details 
    )