from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy import insert, update
from fastapi import HTTPException, status
from jose import JWTError
from db.db_setup import database

from db.models.user import User, Role
from pydantic_shemas.user import UserIn, UserFetch
from api.utils.security import get_password_hash, decode_access_token


async def get_users(skip: int, limit: int):
    query = select(User).limit(limit).offset(skip)
    return await database.fetch_all(query)


async def get_user(username: str):
    query = select(User).where(User.username==username)
    return await database.fetch_one(query)


async def get_user_by_email(email: str):
    query = select(User).where(User.email==email)
    user = await database.fetch_one(query)
    return UserFetch.parse_obj(user)


async def create_user(user: UserIn):
    query = insert(User).values(
        username=user.username,
        bio=user.bio,
        role=Role(user.role),
        email=user.email,
        hashed_password=get_password_hash(user.password),
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow()
    )
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


async def update_user(username: str, user: UserIn):
    query = update(User).where(User.username==username).values(
        username=user.username,
        bio=user.bio,
        role=Role(user.role),
        email=user.email,
        hashed_password=get_password_hash(user.password),
        updated_at = datetime.utcnow()
    )        
    await database.execute(query)
    return {**user.dict()}


async def get_current_user(token: str):
    exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials"
    )
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if email is None:
            raise exp
    except JWTError:
        raise exp
    user = await get_user_by_email(email=email)
    if user is None:
        raise exp
    return user
