import fastapi
from fastapi import HTTPException, Depends, status

from pydantic_shemas.review import ReviewBase, Review
from db.models.review import Title
from api.utils.reviews import (get_reviews,
                               create_review, get_review,
                               update_review, delete_review)
from api.utils.security import JWTBearer
from api.utils.users import get_current_user
from api.utils.util_func import check_if_exists


router = fastapi.APIRouter()

@router.get("/titles/{title_id}/reviews", response_model=list[Review])
async def read_reviews(title_id: int):
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    return await get_reviews(title_id=title_id)

@router.get("/titles/{title_id}/reviews/{review_id}", response_model=Review)
async def read_review(title_id: int, review_id: int):
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    db_review = await get_review(title_id=title_id, review_id=review_id)
    if db_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return db_review

@router.post("/titles/{title_id}/reviews", response_model=Review, dependencies=[Depends(JWTBearer())])
async def create_new_review(title_id: int, review: ReviewBase, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    db_review = await create_review(title_id=title_id, user=current_user, review=review)
    return db_review

@router.patch("/titles/{title_id}/reviews", response_model=Review, dependencies=[Depends(JWTBearer())])
async def update_a_review(title_id: int, review_id: int, review: ReviewBase, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    db_review = await get_review(title_id=title_id, review_id=review_id)
    if db_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    if db_review.author != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    return await update_review(
        title_id=title_id,
        review_id=review_id,
        user=current_user,
        review=review,
        c_date=db_review.created_at,
        )

@router.delete("/titles/{title_id}/reviews/{review_id}", dependencies=[Depends(JWTBearer())])
async def delete_a_review(title_id: int, review_id: int, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    db_review = await get_review(title_id=title_id, review_id=review_id)
    if db_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    if db_review.author != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    await delete_review(title_id=title_id, review_id=review_id)
    return {"status": status.HTTP_204_NO_CONTENT}
