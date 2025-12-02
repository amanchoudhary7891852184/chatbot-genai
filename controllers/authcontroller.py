from sqlalchemy.ext.asyncio import AsyncSession
from schemas import user_schemas
from services import auth_service


async def register(user: user_schemas.UserCreate, db: AsyncSession):
    return await auth_service.register(user, db)


async def login(email: str, password: str, db: AsyncSession):
    return await auth_service.login(email, password, db)






