from pydantic import UUID4
from faststream.rabbit.fastapi import RabbitRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


from app.database import get_async_session
from app.files.utils import delete_old_files_local, S3Client
from app.files.services import delete_file_service
from app.config import settings

broker = RabbitRouter(settings.rabbitmq_url)

scheduler = AsyncIOScheduler()

# Крон для очистки локального диска
async def cleanup_old_files(file_uuid: UUID4, file_extension: str):
    s3_client = S3Client()
    file_key = f"{file_uuid}{file_extension}"
    session = get_async_session()

    print('start cleanup cron task')

    await delete_old_files_local(settings.uploads_dir, settings.FILE_LIFESPAN_LIMIT)
    await delete_file_service(file_uuid, session)
    #Удаление из облака
    await s3_client.delete_file(file_key)

# Настройка планировщика для запуска задачи каждые 10 дней
scheduler.add_job(cleanup_old_files, IntervalTrigger(days=settings.CLEANUP_INTERVAL))


# Задача для загрузки данных в облако
@broker.subscriber("file_upload")
async def upload_to_cloud(message: dict):
    """Сохраняет файл в облаке"""

    # Инициализируем клиента для работы с S3
    s3_client = S3Client()
    
    # Создаем ключ для файла в облаке на основе UUID и расширения
    file_key = f"{message['file_uuid']}{message['file_extension']}"

    try:
        # Вызов метода загрузки файла из S3Client
        await s3_client.upload_file(message['file_path'], file_key)
    except Exception as e:
        raise Exception(f"Ошибка загрузки файла в облако: {str(e)}")