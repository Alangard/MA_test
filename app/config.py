import os
from datetime import timedelta
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class GlobalSettings(BaseSettings):
    DB_HOST: str = os.environ.get("DB_HOST", 'db')
    DB_PORT: str = os.environ.get("DB_PORT", '1221')
    DB_NAME: str = os.environ.get("DB_NAME", 'postgres')
    DB_USER: str = os.environ.get("DB_USER", 'postgres')
    DB_PASS: str = os.environ.get("DB_PASS", 'postgres')

    api_prefix: str = "/api/v1"

    # Настройки для загрузки файлов
    upload_dir: str = os.environ.get('upload_dir', './uploaded_files') # директория на сервере
    FILE_LIFESPAN_LIMIT_DAYS: int = int(os.environ.get('FILE_LIFESPAN_LIMIT_DAYS', 30))
    CLEANUP_INTERVAL: int = int(os.environ.get('CLEANUP_INTERVAL', 10)) # Интервал по очистке файлов (каждые 10 дней)
    FILE_LIFESPAN_LIMIT: timedelta = timedelta(days=FILE_LIFESPAN_LIMIT_DAYS)  # Время жизни файлов  (30 дней)


    # Настройки для RabbitMQ
    RABBITMQ_DEFAULT_USER: str = os.environ.get('RABBITMQ_DEFAULT_USER', 'guest')
    RABBITMQ_DEFAULT_PASS: str = os.environ.get('RABBITMQ_DEFAULT_PASS', 'guest')
    RABBITMQ_PASSWORD: str = os.environ.get('RABBITMQ_PASSWORD', 'pass')
    RABBITMQ_USER: str = os.environ.get('RABBITMQ_USER', 'user')
    RABBITMQ_DEFAULT_VHOST: str = os.environ.get('RABBITMQ_DEFAULT_VHOST', 'rabbitmq')
    RABBITMQ_DEFAULT_PORT: str = os.environ.get('RABBITMQ_DEFAULT_PORT', '5672')
    RABBITMQ_URL: str = f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_DEFAULT_VHOST}'

    # Настройки AWS S3 хранилища
    AWS_ACCESS_KEY_ID: str = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY: str = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_REGION_NAME: str = os.environ.get('AWS_REGION_NAME', '')
    S3_BUCKET_NAME: str = os.environ.get('S3_BUCKET_NAME', '')


settings = GlobalSettings()

