from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict, Field
from datetime import datetime


class FileResponse(BaseModel):
    uuid: UUID4
    original_name: str
    file_size: int
    file_type: str
    extension: str

    model_config = ConfigDict(from_attributes=True)
