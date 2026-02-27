from pydantic import BaseModel, Field
from sqlmodel import SQLModel,Field,Session,create_engine,select,Relationship
from typing import List,Optional

class User(BaseModel):
    name:str
    age:int = Field(..., gt=0, description="Age must be a positive integer")
    email:str

    model_config = {
        "json_schema_extra":{
            "example":{
                "name":"Ramesh",
                "age":30,
                "email":"ramesh@gmail.com"
            }
        }
    }

class BaseUser(BaseModel):
    name:str
    age:int

class FilterParams(BaseModel):
    limit:int = Field(10, gt=0, le=100, description="Limit must be between 1 and 100")
    offset:int = Field(0, ge=0, description="Offset must be a non-negative integer")
    search:str | None = Field(None, description="Search term")

class UserBase(BaseModel):
    username: str
    full_name: str | None = None
    email: str

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

    team: Optional["Team"] = Relationship(back_populates="heros")

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    headquarters: str

    heros: List["Hero"] = Relationship(back_populates="team")
