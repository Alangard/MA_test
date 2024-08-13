from fastapi import APIRouter, UploadFile, File, Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.files.models import FileMetadata
from app.files.schemas import FileResponse
from app.files.services import upload_file_service, get_file_service, delete_file_service

router = APIRouter()

@router.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    response = await upload_file_service(file, session)
    return response

@router.get("/files/{file_uuid}")
async def get_file(file_uuid: UUID4, session: AsyncSession = Depends(get_async_session)):
    response = await get_file_service(file_uuid, session)
    return response

@router.delete("/files/{file_uuid}")
async def delete_file(file_uuid: UUID4, session: AsyncSession = Depends(get_async_session)):
    response = await delete_file_service(file_uuid, session)
    return response