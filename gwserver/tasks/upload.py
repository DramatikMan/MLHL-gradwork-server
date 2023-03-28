import base64

from gwserver.core.s3 import s3


def upload(path: str, content: str) -> None:
    s3.upload(path, base64.b64decode(content.encode("utf-8")))
