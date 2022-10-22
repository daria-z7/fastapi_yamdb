from typing import Optional
from enum import Enum

from pydantic import BaseModel, EmailStr, constr, validator


class UserFetch(BaseModel):
    id: int
    username: str
    bio: Optional[str] = None
    role: Enum
    email: EmailStr
    hashed_password: str


    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    username: str
    bio: Optional[str] = None
    role: str
    email: EmailStr

    class Config:
        orm_mode = True


class User(BaseUser):
    id: Optional[str] = None
    hashed_password: str


class UserIn(BaseUser):
    password: constr(min_length=6)
    password2: str
    role: str

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords don't match")
        return v
    
    @validator("role")
    def check_role(cls, v):
        if v not in ['admin', 'moderator', 'user']:
            raise ValueError("Such role doesn't exist")
        return v
