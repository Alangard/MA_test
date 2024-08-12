from datetime import timedelta
from pydantic_settings import BaseSettings, SettingsConfigDict


class GlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "postgres"
    
    api_prefix: str = "/api/v1"

    # Настройки для загрузки файлов
    upload_dir: str = './uploaded_files' # директория на сервере
    FILE_LIFESPAN_LIMIT_DAYS: int = 30
    FILE_LIFESPAN_LIMIT: timedelta = timedelta(days=FILE_LIFESPAN_LIMIT_DAYS)  # Время жизни файлов  (30 дней)
    CLEANUP_INTERVAL: int = 10 # Интервал по очистке файлов (каждые 10 дней)


    # Настройки для RabbitMQ
    RABBITMQ_USER: str = 'guest'
    RABBITMQ_PASSWORD: str = 'guest'
    RABBITMQ_HOST: str = 'localhost'
    RABBITMQ_PORT: str = '5672'
    RABBITMQ_URL: str = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}'

    # Настройки AWS S3 хранилища
    AWS_ACCESS_KEY_ID: str = ''
    AWS_SECRET_ACCESS_KEY: str =''
    AWS_REGION_NAME: str = ''
    S3_BUCKET_NAME: str = ''


settings = GlobalSettings()

