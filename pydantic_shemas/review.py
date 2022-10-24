from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr, validator


class GenreBase(BaseModel):
    slug: constr(regex="^[-a-zA-Z0-9_]+$")

    class Config:
        orm_mode = True


class GenreCreate(GenreBase):
    name: str

    class Config:
        orm_mode = True


class Genre(GenreCreate):
    id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    slug: constr(regex="^[-a-zA-Z0-9_]+$")


class CategoryCreate(CategoryBase):
    name: str

    class Config:
        orm_mode = True


class Category(CategoryCreate):
    id: int

    class Config:
        orm_mode = True


class TitleBase(BaseModel):
    name: str
    year: int
    description: str | None = None

    @validator('year')
    def check_year(cls, v):
        if v <= 1701:
            raise ValueError("We don't store titles yearlier XVII century.")
        if v > datetime.now().year:
            raise ValueError("The year of the title cannot be in the future.")
        return v


class TitleCreate(TitleBase):
    category: str
    genre: list[str]


class Title(TitleBase):
    id: int
    genre: list[GenreBase]
    category: str
    rating: int | None

    @validator('rating')
    def check_rating(cls, v):
        if v is None:
            return 0
        return round(v)

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    text: str
    score: int

    @validator('score')
    def check_score(cls, v):
        if v < 1 or v > 10:
            raise ValueError("Score should be in range 1-10")
        return v


class Review(ReviewBase):
    id: int
    author: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ReviewFull(ReviewBase):
    id: int
    author_id: int
    title_id: int
    created_at: Optional[datetime] = None
    updated_at: datetime

class CommentBase(BaseModel):
    text: str


class Comment(CommentBase):
    id: int
    author: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CommentFull(CommentBase):
    id: int
    author_id: int
    review_id: int
    created_at: Optional[datetime] = None
    updated_at: datetime

    class Config:
        orm_mode = True
