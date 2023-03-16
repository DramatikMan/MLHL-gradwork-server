from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from gwserver.core.config import config


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self) -> None:
        conn_string = f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PWD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"  # noqa: E501
        self.engine = create_engine(url=conn_string)
        self.make_session = sessionmaker(bind=self.engine)

    def __call__(self) -> Generator[Session, None, None]:
        session = self.make_session()

        try:
            yield session
        finally:
            session.close()


DB = Database()
