from apscheduler.triggers.interval import IntervalTrigger
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.files.utils import delete_old_files_local, S3Client
from app.config import settings

scheduler = AsyncIOScheduler()

broker = RabbitBroker(url=settings.RABBITMQ_URL) 
exch = RabbitExchange("exchange", auto_delete=False)
upload_file_queue = RabbitQueue("upload_file_queue", auto_delete=False)

# Крон для очистки локального диска
async def cleanup_old_files():
    await delete_old_files_local(settings.uploads_dir, settings.FILE_LIFESPAN_LIMIT)


# Настройка планировщика для запуска задачи каждые 10 дней
scheduler.add_job(cleanup_old_files, IntervalTrigger(days=settings.CLEANUP_INTERVAL))


# # Задача для загрузки данных в облако
@broker.subscriber(upload_file_queue, exch)
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