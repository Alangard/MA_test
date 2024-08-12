from typing import Optional
from pydantic import UUID4, BaseModel, Field
from datetime import datetime


class FileResponse(BaseModel):
    uuid: UUID4
    original_name: str
    file_size: int
    file_type: str
    extension: str

    class Config:
        model_config = {'from_attributes': True}