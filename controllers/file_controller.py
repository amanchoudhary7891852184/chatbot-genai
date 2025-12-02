from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.file import UploadedFile
from services.vector_store import add_file_to_vector_store
import shutil
import os
from schemas import file_schemas

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_file(file: UploadFile, user_id: int, db: AsyncSession):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Add to DB
    new_file = UploadedFile(filename=file.filename, file_path=file_path, user_id=user_id)
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    
    # Add to Vector Store
    try:
        add_file_to_vector_store(file_path)
    except Exception as e:
        # Consider if we should rollback DB here or just log error
        # For now, we'll raise error but keep DB record (or maybe delete it?)
        raise HTTPException(status_code=500, detail=f"Error indexing file: {str(e)}")
    
    return file_schemas.UploadResponse(
        message="File uploaded and indexed successfully",
        file=file_schemas.FileResponse.model_validate(new_file)
    )

async def delete_file(file_id: int, user_id: int, db: AsyncSession):
    from sqlalchemy import select
    result = await db.execute(select(UploadedFile).where(UploadedFile.id == file_id, UploadedFile.user_id == user_id))
    file = result.scalars().first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Remove from Disk
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    # Remove from DB
    await db.delete(file)
    await db.commit()
    
    return {"message": "File deleted successfully"}
