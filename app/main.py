from fastapi import FastAPI
from app.routers.users import router as users_router

app = FastAPI()

app.include_router(users_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"health": "Server is running"}
