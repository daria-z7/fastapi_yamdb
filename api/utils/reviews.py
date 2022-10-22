from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy import update, delete, insert

from db.models.review import Review
from db.models.user import User
from pydantic_shemas.review import ReviewBase, ReviewFull
from db.db_setup import database


async def get_reviews(title_id: int):
    query = select(
        Review, User.username.label('author')
        ).join(Review.author).where(Review.title_id==title_id)
    return await database.fetch_all(query)

async def get_review(title_id: int,  review_id: int):
    query = select(
        Review, User.username.label('author')
        ).join(Review.author).where(
        Review.id==review_id,
        Review.title_id==title_id
        )
    return await database.fetch_one(query)

async def create_review(user: dict, review: ReviewBase, title_id: int):
    query = ReviewFull(
        id=0,
        text=review.text,
        score=review.score,
        title_id=title_id,
        author_id=user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    values = {**query.dict()}
    values.pop("id", None)
    query = insert(Review).values(**values)    
    last_record_id = await database.execute(query)
    return {**values, "id": last_record_id, "author": user.username,}

async def update_review(
    title_id: int,
    review_id: int,
    user: dict,
    review: ReviewBase,
    c_date: datetime,
):
    query = ReviewFull(
        id=review_id,
        text=review.text,
        score=review.score,
        title_id=title_id,
        author_id=user.id,
        updated_at=datetime.utcnow()
    )
    values = {**query.dict()}
    values.pop("id", None)
    values.pop("title", None)
    values.pop("author", None)
    values.pop("created_at", None)
    review = update(Review).where(Review.id==review_id).values(**values)
    await database.execute(review)
    return {**values, "id": review_id, "author": user.username, "created_at": c_date}

async def delete_review(title_id: int,  review_id: int):
    query = delete(Review).where(
        Review.id==review_id,
        Review.title_id==title_id
    )
    await database.execute(query)
    return
