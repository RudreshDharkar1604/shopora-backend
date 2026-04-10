from fastapi import HTTPException,Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from utlis.jwt_token import verify_access_token
from constants.auth import allowed_urls

# async def auth_middleware(request,call_next):
#     try:
#         auth_header = request.headers.get("Authorization")
#         if auth_header and auth_header.startswith("Bearer "):
#             token = auth_header.split(" ")[1]
#             payload = await verify_access_token(token)
#             if payload:
#                 request.state.user = payload.get("sub")
#                 call_next()
#             else:
#                 request.state.user = None
#                 raise HTTPException(status_code=400,detail="Unauthenticated Access token is required ")
            
#     except Exception as e:
#         raise HTTPException(status_code=400,detail=[str(e)])

class AuthMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request : Request , call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
        path = request.url.path.rstrip("/")
        if any(path == url.rstrip("/") for url in allowed_urls):
            print("Allowed path", path)
            return await call_next(request)
        print("Current path is ",request.url.path)
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail":"Not authenticated"}
            )
        try:
            token = auth_header.split(" ")[1]
            payload = verify_access_token(token)
            request.state.user = payload.get('sub')
            request.state.role = payload.get('role')
        except Exception as e:
            return JSONResponse(
                status_code=400,
                content={"detail":"Invalid or expired token"}
            )