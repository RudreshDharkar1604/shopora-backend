from fastapi import FastAPI
from db.database import Base, engine
from models import user
from routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth")

@app.get("/hello")
def root():
    return {"message": "Welcome to SHOPORA.."}