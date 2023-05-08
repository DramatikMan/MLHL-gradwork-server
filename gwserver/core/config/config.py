from typing import Any

from pydantic import BaseSettings, PrivateAttr


class Settings(BaseSettings):
    # API
    API_ROOT_PATH: str = ""
    API_WORKERS: int = 4
    API_PORT: int = 8080

    # database
    DB_USER: str = "postgres"
    DB_PWD: str = "postgres"
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"
    _DB_URL: str = PrivateAttr()

    # S3
    S3_URL: str = "https://storage.yandexcloud.net"
    S3_ID: str = ""
    S3_SECRET: str = ""
    S3_BUCKET: str = "gwserver"
    S3_USER_DATA_SUBPATH: str = "userdata"

    # RabbitMQ
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PWD: str = "guest"
    RABBITMQ_HOST: str = "broker"
    RABBITMQ_PORT: int = 5672
    _RABBITMQ_URL: str = PrivateAttr()

    # model
    MODEL_KEY: str = "model.onnx"
    MODEL_VOLUME: str = "/tmp/model"
    _MODEL_FNAME: str = PrivateAttr("model.onnx")

    class Config:
        env_prefix = "GWSERVER_"

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._DB_URL = f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"  # noqa: E501
        self._RABBITMQ_URL = f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PWD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"  # noqa: E501


config = Settings()
