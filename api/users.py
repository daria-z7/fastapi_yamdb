import fastapi
from fastapi import HTTPException, Depends, status

from pydantic_shemas.user import UserIn, BaseUser, UserFetch
from api.utils.users import get_users, get_user, create_user, update_user
from db.db_setup import LIMIT, SKIP
from api.utils.security import JWTBearer
from api.utils.users import get_current_user
from api.utils.permissions import verify_role


router = fastapi.APIRouter()
limit = LIMIT
skip = SKIP

@router.get("/users", response_model=list[BaseUser], dependencies=[Depends(JWTBearer())])
async def read_users(
    token: str = Depends(JWTBearer()),
    skip: int = skip,
    limit: int = limit
):
    current_user = await get_current_user(token=token)
    verify_role(["admin"], current_user)
    db_users = await get_users(skip=skip, limit=limit)
    return db_users


@router.get("/users/me", response_model=UserFetch)
async def get_my_profile(token: str = Depends(JWTBearer())):
    return await get_current_user(token=token)


@router.get("/users/{username}", response_model=BaseUser)
async def read_user(username: str, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    verify_role(["admin"], current_user)
    user = await get_user(username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/users", response_model=BaseUser, dependencies=[Depends(JWTBearer())])
async def create_new_user(user: UserIn, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    verify_role(["admin"], current_user)
    db_user = await create_user(user=user)
    return db_user


@router.patch("/users/{username}", response_model=BaseUser, dependencies=[Depends(JWTBearer())])
async def update_a_user(username: str, user: UserIn, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    verify_role(["admin"], current_user)
    db_user = await get_user(username=username)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db_user = await update_user(username=username, user=user)
    return db_user
