from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import file_controller
from utils.deps import get_current_user
from schemas import file_schemas

router = APIRouter()

@router.post("/upload", response_model=file_schemas.UploadResponse)
async def upload_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await file_controller.upload_file(file, current_user.id, db)

@router.delete("/delete/{file_id}")
async def delete_file(file_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await file_controller.delete_file(file_id, current_user.id, db)
