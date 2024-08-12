from sqlalchemy import UUID, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import BaseModel

class FileMetadata(BaseModel):
    __tablename__ = "file_metadata"

    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True)
    original_name: Mapped[str] = mapped_column(String(250), index=True)
    file_size: Mapped[int] = mapped_column(Integer)
    file_type: Mapped[str] = mapped_column(String(250))
    extension: Mapped[str] = mapped_column(String(20))