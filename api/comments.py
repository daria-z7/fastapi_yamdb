import fastapi
from fastapi import HTTPException, Depends, status

from pydantic_shemas.review import CommentBase, Comment
from api.utils.comments import (get_comments, create_comment,
                               get_comment, update_comment, delete_comment)
from db.models.review import Title, Review
from api.utils.security import JWTBearer
from api.utils.users import get_current_user
from api.utils.util_func import check_if_exists


router = fastapi.APIRouter()

@router.get("/titles/{title_id}/reviews/{review_id}/comments", response_model=list[Comment])
async def read_comments(title_id: int, review_id: int):
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    if not await check_if_exists(Review, review_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return await get_comments(review_id=review_id)

@router.get("/titles/{title_id}/reviews/{review_id}/comments/{comment_id}", response_model=Comment)
async def read_comment(title_id: int, review_id: int, comment_id: int):
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    if not await check_if_exists(Review, review_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    db_comment = await get_comment(review_id=review_id, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return db_comment

@router.post("/titles/{title_id}/reviews/{review_id}/comments", response_model=Comment, dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
async def create_new_comment(title_id: int, review_id: int, comment: CommentBase, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    if not await check_if_exists(Review, review_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return await create_comment(review_id=review_id, comment=comment, user=current_user)

@router.patch("/titles/{title_id}/reviews/{review_id}/comments/{comment_id}", response_model=Comment, tags=["comments"], dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
async def update_a_comment(title_id: int, review_id: int, comment_id: int, comment: CommentBase, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    if not await check_if_exists(Review, review_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    db_comment = await get_comment(review_id=review_id, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if db_comment.author != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    return await update_comment(
        comment_id=comment_id,
        review_id=review_id,
        comment=comment,
        user=current_user,
        c_date=db_comment.created_at,)

@router.delete("/titles/{title_id}/reviews/{review_id}/comments/{comment_id}", dependencies=[Depends(JWTBearer())])
async def delete_a_comment(title_id: int, review_id: int, comment_id: int, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    if not await check_if_exists(Title, title_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    if not await check_if_exists(Review, review_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    db_comment = await get_comment(review_id=review_id, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if db_comment.author != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    await delete_comment(comment_id=comment_id, review_id=review_id)
    return {"status": status.HTTP_204_NO_CONTENT}
