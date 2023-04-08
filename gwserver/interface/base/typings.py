from typing import Protocol, TypeVar

from pydantic import BaseModel


class PMapper(Protocol):
    __tablename__: str


Mapper = TypeVar("Mapper", bound=PMapper)
ResponseOne = TypeVar("ResponseOne", bound=BaseModel, covariant=True)
ResponseList = TypeVar("ResponseList", bound=BaseModel)
