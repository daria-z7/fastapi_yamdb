from fastapi import FastAPI
import uvicorn

from db.db_setup import engine, database
from db.models import user, review
from api import reviews, users, auth, genres, categories, titles, comments


user.Base.metadata.create_all(bind=engine)
review.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="FastAPI_yamdb",
    description="Server for posting comments and giving reviews",
    version="0.0.2",
    license_info={
        "name": "BSD-3",
    }
    )

app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, tags=["users"])
app.include_router(genres.router, tags=["genres"])
app.include_router(categories.router, tags=["categories"])
app.include_router(titles.router, tags=["titles"])
app.include_router(reviews.router, tags=["reviews"])
app.include_router(comments.router, tags=["comments"])

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True, debug=True)
