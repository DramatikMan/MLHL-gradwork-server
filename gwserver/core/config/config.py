from pydantic import BaseSettings, PrivateAttr


class Settings(BaseSettings):
    # API
    API_ROOT_PATH: str = ""
    API_WORKERS: int = 4
    API_PORT: int = 8000

    # database
    DB_URL: str

    # S3
    S3_URL: str
    S3_ID: str
    S3_SECRET: str
    S3_BUCKET: str
    S3_USER_DATA_SUBPATH: str = "userdata"

    # RabbitMQ
    RABBITMQ_HOST: str = "broker"

    # model
    MODEL_KEY: str = "model.onnx"
    MODEL_VOLUME: str = "/tmp/model"
    MODEL_FNAME: str = PrivateAttr("model.onnx")

    class Config:
        env_prefix = "GWSERVER_"


config = Settings()  # type: ignore[call-arg]
