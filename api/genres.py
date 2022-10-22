import fastapi
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic_shemas.review import Genre, GenreCreate
from api.utils.genres import get_genres, get_genre, create_genre
from db.db_setup import get_db, get_async_db
from api.utils.security import JWTBearer
from api.utils.permissions import verify_role
from api.utils.users import get_current_user


router = fastapi.APIRouter()

@router.get("/genres", response_model=list[Genre])
async def read_genres():
    db_genres = await get_genres()
    return db_genres

@router.get("/genres/{genre_id}", response_model=Genre)
async def read_genre(genre_id: int):
    db_genre = await get_genre(genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return db_genre

@router.post("/genres", response_model=Genre, dependencies=[Depends(JWTBearer())])
async def create_new_genre(genre: GenreCreate, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    verify_role(["admin"], current_user)
    db_genre = await create_genre(genre=genre)
    return db_genre
