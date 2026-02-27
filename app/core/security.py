from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "f68e87badc009d4924f775a0185e6ec2698370963aceace44989f49253e7fc8c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str, hashed_password:str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password:str)-> str:
    return pwd_context.hash(password)

def create_access_token(data:dict, expires_delta:timedelta | None = None)-> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt