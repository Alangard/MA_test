from fastapi import FastAPI
from contextlib import asynccontextmanager
from faststream import FastStream

from app.config import settings
from app.database import BaseModel, engine
from app.files.router import router as files_router
from app.files.tasks import broker, scheduler



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async context manager for startup and shutdown lifecycle events.
    - Creates database tables.
    - Sets up bot commands and webhook.

    Yields control during application's lifespan and performs cleanup on exit.
    - Disposes all database connections.
    - Deletes bot webhook and commands.
    - Closes aiohttp session
    """ 

    # При создании приложения
    async with engine.begin() as connection:
        # Создаём таблицы
        await connection.run_sync(BaseModel.metadata.create_all)

    #Подключение RabbitMQ и запуск планировщика задач
    await broker.connect()
    scheduler.start()
    
    try:
        yield
    finally:
        # Отключаемся от RabbitMQ, останавливаем движок БД и планировщик периодических задач
        scheduler.shutdown()
        await broker.disconnect()
        await engine.dispose()

faststream_app = FastStream(broker)

application = FastAPI(title="MA_test", lifespan=lifespan)
application.include_router(files_router, prefix=settings.api_prefix)