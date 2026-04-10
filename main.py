from fastapi import FastAPI
from sqlalchemy import text
from core.config import settings
from db.database import engine
from routes import auth
from middlewares.auth import AuthMiddleWare
from exceptions.base_excpetion import BaseException
from core.exception_handler import app_exception_handler
import logging

# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app_logger")


app = FastAPI(
    title="SHOPORA API",
    description="API for SHOPORA e-commerce platform",
    version="1.0.0",
    docs_url="/docs",
)


# --------------------------------------------------
# Startup Event (Check DB Connection)
# --------------------------------------------------
@app.on_event("startup")
async def startup():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(" Database connection failed")
        logger.error(str(e))

# --------------------------------------------------
# Shutdown Event
# --------------------------------------------------
@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
    logger.info(" Database connection closed")

# --------------------------------------------------
# Health Check Endpoint
# --------------------------------------------------
@app.get("/health")
async def health_check():
    return {
        "status": "OK",
        "message": "Sistema Contable funcionando correctamente"
    }

# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------
@app.get("/")
async def root():
    return {
        "app": "Contabilidad API",
        "version": "1.0.0"
    }

# --------------------------------------------------
# Include Middlewares  
# --------------------------------------------------
app.add_middleware(AuthMiddleWare)

# --------------------------------------------------
# Include Exception Handler  
# --------------------------------------------------
app.add_exception_handler(BaseException, app_exception_handler)
# --------------------------------------------------
# Include Routers 
# --------------------------------------------------
app.include_router(auth.router, prefix="/auth", tags=["Authentication Routers"])