import io

from boto3 import session

from gwserver.core import config


class S3:
    def __init__(self) -> None:
        self.bucket = config.S3_BUCKET
        self.session = session.Session()

        self.client = self.session.client(
            "s3",
            endpoint_url=config.S3_URL,
            aws_access_key_id=config.S3_ID,
            aws_secret_access_key=config.S3_SECRET,
            verify=False,
        )

    def download(self, key: str) -> bytes:
        response = self.client.get_object(Bucket=self.bucket, Key=key)
        data: bytes = response["Body"].read()

        return data

    def upload(self, key: str, content: bytes) -> None:
        self.client.upload_fileobj(io.BytesIO(content), self.bucket, key)


s3 = S3()
