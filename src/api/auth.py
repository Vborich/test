from fastapi import APIRouter

from src.application.auth.models.UserLogin import UserLogin
from src.application.auth.models.Token import Token
from src.application.auth.services.authService import (authenticate_user, create_access_token)

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)


@router.post("/login")
async def login(user_login: UserLogin) -> Token:
    user = await authenticate_user(user_login)
    access_token = create_access_token(data={"id": str(user.id)})
    return Token(access_token=access_token)
