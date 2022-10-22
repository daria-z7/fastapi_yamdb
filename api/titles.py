import fastapi
from fastapi import HTTPException, Depends, status

from pydantic_shemas.review import Title, TitleCreate
from api.utils.titles import (get_titles, get_title, create_title,
                               delete_title, update_title)
from api.utils.security import JWTBearer
from api.utils.permissions import verify_role
from api.utils.users import get_current_user
from api.utils.util_func import check_if_exists


router = fastapi.APIRouter()

@router.get("/titles")
async def read_titles():
    db_titles = await get_titles()
    print(db_titles)
    return db_titles

@router.get("/titles/{title_id}")
async def read_title(title_id: int):
    db_title = await get_title(title_id=title_id)
    if db_title is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Title not found"
        )
    print(db_title)
    return db_title

@router.post("/titles", response_model=Title, dependencies=[Depends(JWTBearer())])
async def create_new_title(title: TitleCreate, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    verify_role(["admin"], current_user)
    return await create_title(title=title)

@router.delete("/titles/{title_id}", dependencies=[Depends(JWTBearer())])
async def delete_a_title(title_id: int, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    verify_role(["admin"], current_user)
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    await delete_title(title_id=title_id)
    return {"status": status.HTTP_204_NO_CONTENT}

@router.patch("/titles/{title_id}", response_model=Title, dependencies=[Depends(JWTBearer())])
async def update_a_title(title_id: int, title: TitleCreate, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    verify_role(["admin"], current_user)
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    return await update_title(title_id=title_id, title=title)
