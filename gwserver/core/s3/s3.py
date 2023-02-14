import io
from typing import Protocol

from boto3 import session

from gwserver.core import config


class Reader(Protocol):
    def read(self) -> bytes:
        ...


class S3:
    def __init__(self) -> None:
        self.bucket = config.S3_BUCKET
        self.session = session.Session()

        self.client = self.session.client(
            "s3",
            endpoint_url=config.S3_URL,
            aws_access_key_id=config.S3_ID,
            aws_secret_access_key=config.S3_SECRET,
        )

    def reader(self, key: str) -> Reader:
        response = self.client.get_object(Bucket=self.bucket, Key=key)
        body: Reader = response["Body"]

        return body

    def download(self, key: str) -> bytes:
        return self.reader(key).read()

    def upload(self, key: str, content: bytes) -> None:
        self.client.upload_fileobj(io.BytesIO(content), self.bucket, key)


s3 = S3()
