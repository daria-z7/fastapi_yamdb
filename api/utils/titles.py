from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, insert, update, delete
from sqlalchemy.future import select

from db.models.review import (Genre, Category, Title,
                              genre_title_table, Review)
from pydantic_shemas.review import TitleCreate
from db.db_setup import database


async def get_titles():
    # sq_rating = db.query(
    #     Review.title_id, func.avg(Review.score).label("rating")
    #     ).group_by(Review.title_id).subquery()
    # query = db.query(
    #     Title,
    #     sq_rating.c.rating
    #     ).outerjoin(
    #         sq_rating,
    #         Title.id==sq_rating.c.title_id
    #     ).all()
    sq_rating = select(
        Review.title_id, func.avg(Review.score).label("rating")
        ).group_by(Review.title_id).subquery()
    query = select(
        Title,
        sq_rating.c.rating
        ).outerjoin(
            sq_rating,
            Title.id==sq_rating.c.title_id
        )
    # query_rating = []
    # for obj, rating in query:
    #     obj.rating = rating
    #     query_rating.append(obj)
    print(query)
    return await database.fetch_all(query)

async def get_title(title_id: int):
    # sq_rating = db.query(
    #     Review.title_id, func.avg(Review.score).label("rating")
    #     ).group_by(Review.title_id).subquery()
    # query = db.query(
    #     Title,
    #     sq_rating.c.rating
    #     ).outerjoin(
    #         sq_rating,
    #         Title.id==sq_rating.c.title_id
    #     ).filter(Title.id==title_id).first()
    # query[0].rating = query[1]
    sq_rating = select(
        Review.title_id, func.avg(Review.score).label("rating")
        ).group_by(Review.title_id).subquery()
    query = select(
        Title,
        sq_rating.c.rating
        ).outerjoin(
            sq_rating,
            Title.id==sq_rating.c.title_id
        ).where(Title.id==title_id)
    return await database.fetch_one(query)

async def create_title(title: TitleCreate):
    if await database.fetch_val(select(func.count(Title.id)).where(
        Title.name==title.name,
        Title.year==title.year
        )) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title with this name and year already exists"
        )
    category = await database.fetch_one(
        select(Category).where(Category.slug==title.category)
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category {title.category} doesn't exist."
        )
    for genre in title.genre:
        if await database.fetch_val(
            select(func.count(Genre.id)).filter(Genre.slug==genre)
        ) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Genre {genre} doesn't exist."
            )
    genres = await database.fetch_all(select(Genre).where(Genre.slug.in_(title.genre)))
    print(category)
    print(genres)
    query = Title(
        name=title.name,
        year=title.year,
        description=title.description,
        #genre=genres,
        category_id=category.id,
    )
    print(query.genre)
    for genre in genres:
        print(genre)
        query.genre.append(genre)
    #last_record = await database.execute(query)
    #print(last_record)
    print(query.id)
    return {**title.dict(), "id": 6, "category": category, "genre": genres}


async def delete_title(title_id: int):
    query = delete(Title).where(Title.id==title_id)
    await database.execute(query)
    return

async def update_title(db: Session, title: TitleCreate, title_id: int):
    category = db.query(Category).filter(Category.slug==title.category).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category {title.category} doesn't exist."
        )
    for genre in title.genre:
        if not db.query(Genre).filter(Genre.slug==genre).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Genre {genre} doesn't exist."
            )
    genres = db.query(Genre).filter(Genre.slug.in_(title.genre))
    db_title = Title(
        id=title_id,
        name=title.name,
        year=title.year,
        description=title.description,
        category=category,
    )
    db.query(genre_title_table).filter(
        genre_title_table.c.title_id==title_id
    ).delete()
    db.commit()
    for genre in genres:
        db_title.genre.append(genre)
    values = db_title.__dict__
    values.pop("id", None)
    title = db.query(Title).filter(Title.id==title_id).first()
    for (key, value) in values.items():
        if key in title.__mapper__.attrs.keys():
            setattr(title, key, value)
            db.commit()
    return title
