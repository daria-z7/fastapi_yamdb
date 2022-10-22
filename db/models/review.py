from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from db.db_setup import Base
from .mixins import Timestamp


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False)


genre_title_table = Table(
    "association",
    Base.metadata,
    Column("genre_id", ForeignKey("genres.id")),
    Column("title_id", ForeignKey("titles.id")),
)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False)


class Title(Base):
    __tablename__ = "titles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    description = Column(String)
    genre = relationship("Genre", secondary=genre_title_table, backref="titles")
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    category = relationship("Category", backref="titles")


class Review(Timestamp, Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    author = relationship("User", backref="reviews")
    score = Column(Integer)
    title_id = Column(Integer, ForeignKey("titles.id", ondelete="CASCADE"), nullable=False)
    title = relationship("Title", backref="reviews")


class Comment(Timestamp, Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    author = relationship("User", backref="comments")
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    review = relationship("Review", backref="reviews")
