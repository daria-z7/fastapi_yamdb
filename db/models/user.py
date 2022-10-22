import enum

from sqlalchemy import Column, Integer, String, Enum

from db.db_setup import Base
from .mixins import Timestamp


class Role(enum.Enum):
    admin = 'admin'
    moderator = 'moderator'
    user = 'user'


class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    bio = Column(String(225))
    hashed_password = Column(String)
    role = Column(Enum(Role))
