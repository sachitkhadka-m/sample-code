from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_db
from app.crud.user import create_user, authenticate_user
from app.core.security import create_access_token
from app.schemas.user import UserCreate,UserRead
from app.schemas.token import TokenData as Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register",response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token,"type":"bearer"}