from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password:str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class AddressCreate(BaseModel):
    street: str  
    city: str



