import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DB_URL = "postgresql+psycopg2://fast_user:fast_user@localhost/fapi_yamdb"
ASYNC_SQLALCHEMY_DB_URL = "postgresql+asyncpg://fast_user:fast_user@localhost/fapi_yamdb"
SECRET_KEY = "99f454b38b87384ea8ae64e62e6db312134320175bf2bdfcdb7f82944e9a6948"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1360
LIMIT = 10
SKIP = 0

database = databases.Database(ASYNC_SQLALCHEMY_DB_URL)
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={}, future=True)
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()
