from pydantic import BaseSettings


class Settings(BaseSettings):
    # API
    API_ROOT_PATH: str = ""
    API_PORT: int = 8000

    # database
    DB_URL: str

    class Config:
        env_prefix = "GW_"


config = Settings()
