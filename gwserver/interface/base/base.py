from abc import abstractmethod
from typing import Protocol, Type

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ColumnElement

from gwserver.schema import error

from .typings import Mapper, ResponseList, ResponseOne


class Base(Protocol[Mapper, ResponseOne]):
    @property
    @abstractmethod
    def _mapper(self) -> Type[Mapper]:
        ...

    @property
    @abstractmethod
    def _response_schema_one(self) -> Type[ResponseOne]:
        ...

    @classmethod
    @abstractmethod
    def _to_json(cls, rec: Mapper) -> ResponseOne:
        ...

    @classmethod
    @abstractmethod
    def _where_uid(cls, uid: int) -> ColumnElement[bool]:
        """Primary key value equality expression."""
        ...

    def _select_where_uid(self, uid: int, session: Session) -> Mapper:
        stmt = select(self._mapper).where(self._where_uid(uid))
        existing: Mapper | None = session.scalar(stmt)

        if existing is None:
            raise error.NotFoundByUID

        return existing

    def get(self, uid: int, session: Session) -> ResponseOne:
        return self._to_json(self._select_where_uid(uid, session))


class Listable(Base[Mapper, ResponseOne], Protocol[Mapper, ResponseOne, ResponseList]):
    @property
    @abstractmethod
    def _response_schema_list(self) -> Type[ResponseList]:
        ...

    @classmethod
    @abstractmethod
    def _to_json_list(cls, rec: Mapper) -> ResponseList:
        ...

    def ls(self, session: Session) -> list[ResponseList]:
        stmt = select(self._mapper)
        result = session.scalars(stmt)

        return [self._to_json_list(i) for i in result]
