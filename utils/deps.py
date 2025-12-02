from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import Users
from schemas.user_schemas import User
from utils.security import verify_password
from utils.jwt import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_access_token(token)
    if not payload or "user_id" not in payload:
        raise credentials_exception

    user_id = payload["user_id"]

    # Async query
    from sqlalchemy.future import select
    result = await db.execute(select(Users).filter(Users.id == user_id))
    user = result.scalars().first()
    if not user:
        raise credentials_exception

    return User.model_validate(user)
