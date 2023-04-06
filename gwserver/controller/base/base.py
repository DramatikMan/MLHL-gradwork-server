from abc import abstractmethod
from typing import Callable, Protocol, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BinaryExpression

from gwserver.schema import error


class Mapper(Protocol):
    __tablename__: str


M = TypeVar("M", bound=Mapper)
R1 = TypeVar("R1", bound=BaseModel, covariant=True)


class Controller(Protocol[M, R1]):
    mapper: Type[M]
    where_one: Callable[[int], BinaryExpression[M]]

    @property
    @abstractmethod
    def response_schema_one(self) -> Type[R1]:
        ...

    @classmethod
    @abstractmethod
    def _JSONify(self, instance: M) -> R1:
        ...

    def get(self, uid: int, session: Session) -> R1:
        stmt = select(self.mapper).where(self.where_one(uid))
        existing: M | None = session.scalar(stmt)

        if existing is None:
            raise error.NOT_FOUND_BY_UID

        return self._JSONify(existing)
