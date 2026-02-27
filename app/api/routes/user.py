from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.schemas.user import UserRead
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
def read_me(current_user = Depends(get_current_user)):
    return current_user


@router.get("/",response_model=list[UserRead])
def read_users(current_user: User =  Depends(get_current_user),db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
