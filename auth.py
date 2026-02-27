from fastapi import FastAPI,Query,File,UploadFile,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from pwdlib import PasswordHash
from pydantic import BaseModel
from typing import Annotated

SECRET_KEY = "f68e87badc009d4924f775a0185e6ec2698370963aceace44989f49253e7fc8c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()

fake_db = {
    "foo": {"username": "foo", "full_name": "Foo20", "email": "foo@gmail.com",
            "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$9H54gAO2SQswx0H8nAzmzA$FImr4Pz0uoM+FoNTjBRG5ei7Iw/N/B9arV1IcyCKFxg",
            "disabled": False},
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = None

class TokenData(BaseModel):
    username: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserInDB(User):
    hashed_password: str

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_user(username: str):
    user = fake_db.get(username)
    if not user:
        return None
    return UserInDB(**user)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@app.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    access_token = jwt.encode({"sub": user.username}, "secret", algorithm="HS256")
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        print('Payload:', payload)
        username: str = payload.get("sub")
        print(username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

