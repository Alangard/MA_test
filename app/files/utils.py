import os
import aiofiles
import aioboto3
from datetime import datetime, timedelta
from app.config import settings



class S3Client:
    def __init__(self):
        self.s3_client = aioboto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME
        )
        self.bucket_name = settings.S3_BUCKET_NAME


    async def upload_file(self, file_path: str, file_key: str):
        print('start upload cloud')
        # async with aiofiles.open(file_path, 'rb') as file:
        #     await self.s3_client.upload_fileobj(file, self.bucket_name, file_key)

    async def delete_file(self, file_key: str):
        print('start delete cloud')
        # await self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_key)


async def delete_old_files_local(directory: str, retention_period: timedelta):
    """Удаляет файлы старше определенного времени из указанной директории."""
    current_datetime = datetime.now()

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            # Получаем время создания файла и преобразуем его в datetime
            file_created_timestamp = os.path.getctime(file_path)
            file_created_datetime = datetime.fromtimestamp(file_created_timestamp)

            # Проверяем, если файл старше retention_period, удаляем его
            if (current_datetime - file_created_datetime) > retention_period:
                try: 
                    os.remove(file_path)

                    print(f"Удален старый файл: {file_path}")
                except Exception as e:
                    print(f"Ошибка при удалении файла {file_path}: {e}")


