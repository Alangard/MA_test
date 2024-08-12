import os
import uuid
import aiofiles

from fastapi import File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.files.models import FileMetadata
from app.files.schemas import FileResponse
from app.config import settings

from app.files.tasks import broker


async def upload_file_service(file: File, session: AsyncSession) -> FileResponse:
    # Генерация уникального идентификатора для файла
    file_uuid = uuid.uuid4()
    file_extension = os.path.splitext(file.filename)[1]
    save_path = f"{settings.upload_dir}/{file_uuid}{file_extension}"

    # Создание директории, если её нет
    os.makedirs(settings.upload_dir, exist_ok=True)

    # Асинхронное сохранение файла на диск
    try:
        async with aiofiles.open(save_path, 'wb') as out_file:
            while True:
                content = await file.read(1024)
                if not content: break
                await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения файла: {str(e)}")
    
    # Сохранение метаданных файла в базе данных
    try:
        file_metadata = FileMetadata(
            uuid=file_uuid,
            original_name=file.filename,
            file_size=file.size,
            file_type=file.content_type,
            extension=file_extension
        )

        session.add(file_metadata)
        await session.commit()
        await session.refresh(file_metadata)

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения метаданных: {str(e)}")

    # Асинхронная отправка файла в облако (отправка задачи в очередь RabbitMQ)
    task_data = {
        "filepath": file.filename,
        "file_uuid": file_uuid,
        "file_extension": file_extension,
    }
    await broker.publish(task_data, "file_upload")

    
    return FileResponse(**file_metadata.__dict__)

async def delete_file_service(file_uuid: str, session: AsyncSession) -> None:
    stmt = select(FileMetadata).where(FileMetadata.uuid == file_uuid)
    result = await session.execute(stmt)
    file_metadata = result.scalars().one_or_none()

    if file_metadata is not None:
        # Удаление записи о файле из базы данных
        await session.delete(file_metadata)
        await session.commit()
        print(f"Метаданные о файле {file_uuid} удалены из БД.")
    else:
        print(f"Файл с указанным UUID: {file_uuid} не был найден в БД")

    return

async def get_file_service(file_uuid: str, session: AsyncSession) -> StreamingResponse:
    stmt = select(FileMetadata).where(FileMetadata.uuid == file_uuid)
    result = await session.execute(stmt)
    file_metadata = result.scalars().one_or_none()

    if file_metadata is None:
        raise HTTPException(status_code=404, detail="Файл не был найден в базе")

    file_path = f"{settings.upload_dir}/{file_metadata.uuid}{file_metadata.extension}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не был найден на сервере")

    # Открытие файла для потоковой передачи
    file = open(file_path, "rb")
    
    # Определение типа содержимого
    media_type = file_metadata.file_type

    # Функция для потокового скачивания файла
    response = StreamingResponse(file, media_type=media_type)

    return response