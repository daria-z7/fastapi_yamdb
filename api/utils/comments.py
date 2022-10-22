from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy import update, delete, insert

from db.models.review import Comment
from db.models.user import User
from pydantic_shemas.review import CommentBase, CommentFull
from db.db_setup import database


async def get_comments(review_id: int):
    query = select(
        Comment, User.username.label('author')
        ).join(Comment.author).where(Comment.review_id==review_id)
    return await database.fetch_all(query)

async def get_comment(review_id: int, comment_id: id):
    query = select(
        Comment, User.username.label('author')
        ).join(
            Comment.author
        ).where(
            Comment.review_id==review_id,
            Comment.id==comment_id
        )
    return await database.fetch_one(query)

async def create_comment(
    user: dict,
    review_id: int,
    comment: CommentBase
):
    query = CommentFull(
        id=0,
        text=comment.text,
        review_id=review_id,
        author_id=user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    values = {**query.dict()}
    values.pop("id", None)
    query = insert(Comment).values(**values)    
    last_record_id = await database.execute(query)
    return {**values, "id": last_record_id, "author": user.username,}

async def update_comment(
    user: dict,
    review_id: int,
    comment_id: int,
    comment: CommentBase,
    c_date: datetime
):
    query = CommentFull(
        id=comment_id,
        text=comment.text,
        review_id=review_id,
        author_id=user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    values = {**query.dict()}
    values.pop("id", None)
    values.pop("title", None)
    values.pop("author", None)
    values.pop("created_at", None)
    comment = update(Comment).where(
        Comment.id==comment_id
    ).values(**values)
    await database.execute(comment)
    return {**values, "id": review_id, "author": user.username, "created_at": c_date}

async def delete_comment(comment_id: int, review_id: int):
    query = delete(
        Comment
        ).where(
            Comment.review_id==review_id,
            Comment.id==comment_id
        )
    await database.execute(query)
    return
