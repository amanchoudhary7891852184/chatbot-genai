from pydantic import BaseModel
from datetime import datetime

class FileBase(BaseModel):
    filename: str
    file_path: str

class FileCreate(FileBase):
    pass

class FileResponse(FileBase):
    id: int
    uploaded_at: datetime
    user_id: int

    model_config = {'from_attributes': True}

class UploadResponse(BaseModel):
    message: str
    file: FileResponse
