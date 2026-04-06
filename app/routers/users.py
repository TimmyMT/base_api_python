from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import UserCreate
from app.services.user_service import create_user

router = APIRouter()

@router.post("/users", status_code=201)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user)
        return {"message": "User created successfully", "user_id": new_user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))