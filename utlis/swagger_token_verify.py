from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

security = HTTPBearer()

async def verify_swagger_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7J3VzZXJfaWQnOiAyLCAnbW9iaWxlX25vJzogOTMyMjk5NjcxMywgJ2VtYWlsJzogJ2JoYWt0aUBnbWFpbC5jb20nLCAnaXNfYWN0aXZlJzogVHJ1ZX0iLCJleHAiOjE3NzYxNzI4OTl9.JnEAzgFXOFbHpZwxNgNafvgjQV-jwBZ7bIB29HxkQn4":
        raise Exception("Invalid token")
    return token