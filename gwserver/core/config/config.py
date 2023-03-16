from pydantic import BaseSettings, PrivateAttr


class Settings(BaseSettings):
    # API
    API_ROOT_PATH: str = ""
    API_WORKERS: int = 4
    API_PORT: int = 8000

    # database
    DB_HOST: str = "postgres"
    DB_USER: str = "postgres"
    DB_PWD: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"

    # S3
    S3_URL: str = "https://storage.yandexcloud.net"
    S3_ID: str
    S3_SECRET: str
    S3_BUCKET: str = "gwserver"
    S3_USER_DATA_SUBPATH: str = "userdata"

    # RabbitMQ
    RABBITMQ_HOST: str = "broker"

    # model
    MODEL_KEY: str = "model.onnx"
    MODEL_VOLUME: str = "/app/model"
    _MODEL_FNAME: str = PrivateAttr("model.onnx")

    class Config:
        env_prefix = "GWSERVER_"


config = Settings()  # type: ignore[call-arg]
