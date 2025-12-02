# routes/user_routes.py
from fastapi import APIRouter, Depends, UploadFile, File, status, Response, HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from schemas.user_schemas import *
from controllers import usercontroller
from utils.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[User])
async def user_list(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await usercontroller.get_users(db)

@router.get("/{user_id}", response_model=User)
async def user_detail(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = await usercontroller.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

