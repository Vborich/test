import uuid
from datetime import datetime, timedelta
from fastapi import Request

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from tortoise.expressions import Q

import src.settings as settings
from src.application.auth.models.UserLogin import UserLogin
from src.models.User import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


async def authenticate_user(user_login: UserLogin):
    user = await User.filter(Q(username=user_login.username) & Q(password=user_login.password)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return user


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token_expired_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer,
            self).__call__(request)

        try:
            token: str = credentials.credentials
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            id: uuid.UUID = payload.get("id")
            exp: float = payload.get("exp")

            if datetime.utcfromtimestamp(exp) < datetime.utcnow():
                raise token_expired_exception

            if id is None:
                raise credentials_exception

        except JWTError:
            raise credentials_exception

        user = await User.filter(id=id).first()

        if user is None:
            raise credentials_exception

        return user
