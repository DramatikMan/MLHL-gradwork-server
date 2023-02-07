from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from gwserver.core.config import config


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self) -> None:
        self.engine = create_engine(url=config.DB_URL)
        self.make_session = sessionmaker(bind=self.engine)

    def __call__(self) -> Generator[Session, None, None]:
        session = self.make_session()

        try:
            yield session
        finally:
            session.close()
