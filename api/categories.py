import fastapi
from fastapi import HTTPException, Depends, status

from pydantic_shemas.review import Category, CategoryCreate
from api.utils.categories import get_categories, get_category, create_category
from api.utils.security import JWTBearer
from api.utils.permissions import verify_role
from api.utils.users import get_current_user


router = fastapi.APIRouter()

@router.get("/categories", response_model=list[Category])
async def read_categories():
    db_categories = await get_categories()
    return db_categories

@router.get("/categories/{category_id}", response_model=Category)
async def read_category(category_id: int):
    db_category = await get_category(category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return db_category

@router.post("/categories", response_model=Category, dependencies=[Depends(JWTBearer())])
async def create_new_category(category: CategoryCreate, token: str = Depends(JWTBearer())):
    current_user = await get_current_user(token=token)
    verify_role(["admin"], current_user)
    db_category = await create_category(category=category)
    return db_category
