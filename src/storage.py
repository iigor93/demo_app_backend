import json
from io import BytesIO
from pathlib import Path
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from fastapi_storages import S3Storage

from src.config import settings


class BannerStorage(S3Storage):
    OVERWRITE_EXISTING_FILES = False
    AWS_ACCESS_KEY_ID = settings.s3_access_key
    AWS_SECRET_ACCESS_KEY = settings.s3_secret_key
    AWS_S3_BUCKET_NAME = settings.s3_bucket
    AWS_S3_ENDPOINT_URL = settings.s3_endpoint
    AWS_S3_USE_SSL = settings.s3_secure
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = ""

    def open(self, name: str) -> BytesIO:
        key = self.get_name(name)
        response = self._s3.get_object(Bucket=self.AWS_S3_BUCKET_NAME, Key=key)
        return BytesIO(response["Body"].read())

    def generate_new_filename(self, filename: str) -> str:
        suffix = Path(filename).suffix.lower()
        return f"{uuid4()}{suffix}"
    
    def get_path(self, name: str) -> str:
        key = self.get_name(name)
        return f"{settings.public_s3_base}/{self.AWS_S3_BUCKET_NAME}/{key}"


banner_storage = BannerStorage()


def ensure_s3_bucket() -> None:
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint,
        use_ssl=settings.s3_secure,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
    )

    try:
        s3_client.head_bucket(Bucket=settings.s3_bucket)
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code", "")
        if error_code not in {"404", "NoSuchBucket"}:
            raise
        s3_client.create_bucket(Bucket=settings.s3_bucket)

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{settings.s3_bucket}/*"],
            }
        ],
    }
    s3_client.put_bucket_policy(Bucket=settings.s3_bucket, Policy=json.dumps(policy))
