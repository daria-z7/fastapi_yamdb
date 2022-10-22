from sqlalchemy import insert
from sqlalchemy.future import select

from db.models.review import Category
from pydantic_shemas.review import CategoryCreate
from db.db_setup import database


async def get_categories():
    query = select(Category)
    return await database.fetch_all(query)


async def get_category(category_id: int):
    query = select(Category).where(Category.id==category_id)
    return await database.fetch_one(query)


async def create_category(category: CategoryCreate):
    query = insert(Category).values(
        name=category.name,
        slug=category.slug
    )        
    last_record_id = await database.execute(query)
    return {**category.dict(), "id": last_record_id}
