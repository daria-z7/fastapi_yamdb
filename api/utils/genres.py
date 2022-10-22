from sqlalchemy import insert
from sqlalchemy.future import select

from db.models.review import Genre
from pydantic_shemas.review import GenreCreate
from db.db_setup import database


async def get_genres():
    query = select(Genre)
    return await database.fetch_all(query)


async def get_genre(genre_id: int):
    query = select(Genre).where(Genre.id==genre_id)
    return await database.fetch_one(query)


async def create_genre(genre: GenreCreate):
    query = insert(Genre).values(
        name=genre.name,
        slug=genre.slug
    )        
    last_record_id = await database.execute(query)
    return {**genre.dict(), "id": last_record_id}
