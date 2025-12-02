from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
import schemas.user_schemas as user_schemas
from controllers import authcontroller
from utils.deps import get_current_user

router = APIRouter()


@router.post("/register", response_model=user_schemas.User)
async def register_user(
    user: user_schemas.UserCreate, db: AsyncSession = Depends(get_db)
):
    return await authcontroller.register(user, db)


@router.post("/login", response_model=user_schemas.TokenResponse)
async def user_login(
    login_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await authcontroller.login(login_data.username, login_data.password, db)






