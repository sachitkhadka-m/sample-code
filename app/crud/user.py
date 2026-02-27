from sqlalchemy.orm import Session
from ..models.user import User, Address
from ..schemas.user import UserCreate, AddressCreate,UserRead
from app.core.security import get_password_hash,verify_password


def create_user(db: Session, user: UserCreate)-> User:
    print('User:',user)
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username,email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_username(db: Session, username: str) -> UserRead | None:
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str) -> UserRead | None:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user