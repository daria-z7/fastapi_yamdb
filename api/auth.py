from fastapi import APIRouter, HTTPException, status

from pydantic_shemas.token import Token, Login
from api.utils.security import verify_password, create_access_token
from api.utils.users import get_user_by_email


router = APIRouter()

@router.post("/", response_model=Token)
async def login(login: Login):
    user = await get_user_by_email(email=login.email)
    if user is None or not verify_password(
        login.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return Token(
        access_token=create_access_token({"sub": user.email}),
        token_type="Bearer"
    )
