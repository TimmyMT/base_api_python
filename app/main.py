from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers.users import router as users_router
from app.routers.sessions import router as sessions_router
from app.routers.categories import router as categories_router
from app.models import User, Role, Category, Permission

from app.seed import run_seed

app = FastAPI()

app.include_router(users_router, prefix="/api/v1")
app.include_router(sessions_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid request data", "errors": exc.errors()},
    )

@app.get("/")
def root():
    return {"health": "Server is running"}

@app.on_event("startup")
def on_startup():
    run_seed()
