from pydantic import BaseSettings


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

    # RabbitMQ
    RABBITMQ_HOST: str

    class Config:
        env_prefix = "GWSERVER_"


config = Settings()
