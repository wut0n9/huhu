from minio import Minio
from app.core.config import settings
import uuid

client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

def upload_file_to_minio(file_bytes: bytes, filename: str) -> str:
    bucket = settings.MINIO_BUCKET
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
    object_name = f"{uuid.uuid4()}_{filename}"
    client.put_object(bucket, object_name, data=bytes(file_bytes), length=len(file_bytes))
    return object_name

def get_file_url(object_name: str) -> str:
    return f"http://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET}/{object_name}" 